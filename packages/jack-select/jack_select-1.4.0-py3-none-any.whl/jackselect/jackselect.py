#!/usr/bin/env python
"""A systray app to set the JACK configuration from QjackCtl presets via DBus."""

import argparse
import logging
import os
import sys

os.environ['NO_AT_BRIDGE'] = "1"  # noqa
import gi
gi.require_version('Gtk', '3.0')  # noqa
from gi.repository import Gtk, GObject

import dbus
from xdg import BaseDirectory as xdgbase

from .alsainfo import AlsaInfo
from .devmonitor import AlsaDevMonitor
from .indicator import Indicator
from .jackcontrol import (JackCfgInterface, JackCtlInterface,
                          get_jack_controller)
from .jackselect_service import DBUS_NAME, DBUS_INTERFACE, DBUS_PATH, JackSelectService
from .qjackctlconf import get_qjackctl_presets
from .version import __version__


log = logging.getLogger('jack-select')

INTERVAL_GET_STATS = 500
INTERVAL_CHECK_CONF = 1000
INTERVAL_RESTART = 1000
DEFAULT_CONFIG = 'rncbc.org/QjackCtl.conf'


class JackSelectApp:
    """A simple systray application to select a JACK configuration preset."""

    def __init__(self, bus=None, config=None, monitor_devices=True, ignore_default=False):
        if bus is None:
            bus = dbus.SessionBus()

        self.monitor_devices = monitor_devices
        self.ignore_default = ignore_default
        self.gui = Indicator('jack.png', "JACK-Select")
        self.gui.set_tooltip(self.tooltip_query)
        self.jack_status = {}
        self.tooltext = "No status available."
        dbus_obj = get_jack_controller(bus)
        self.jackctl = JackCtlInterface(dbus_obj)
        self.jackcfg = JackCfgInterface(dbus_obj)

        if monitor_devices:
            # get ALSA devices and their parameters
            self.handle_device_change(init=True)
        else:
            self.alsainfo = None

        # load QjackCtl presets
        self.config = config

        self.presets = None
        self.active_preset = None
        self.load_presets()

        # set up periodic functions to check presets & jack status
        GObject.timeout_add(INTERVAL_CHECK_CONF, self.load_presets)
        GObject.timeout_add(INTERVAL_GET_STATS, self.get_jack_stats)
        self.jackctl.is_started(self.receive_jack_status)
        self.jackctl.add_signal_handler(self.handle_jackctl_signal)

        # add & start DBUS service
        self.dbus_service = JackSelectService(self, bus)

        if monitor_devices:
            # set up udev device monitor
            self.alsadevmonitor = AlsaDevMonitor(self.handle_device_change)
            self.alsadevmonitor.start()

    def load_presets(self, force=False):
        if self.config in (None, DEFAULT_CONFIG):
            qjackctl_conf = xdgbase.load_first_config(DEFAULT_CONFIG)
        else:
            qjackctl_conf = self.config if os.access(self.config, os.R_OK) else None

        if qjackctl_conf:
            mtime = os.path.getmtime(qjackctl_conf)
            changed = mtime > getattr(self, '_conf_mtime', 0)

            if changed:
                log.debug("Configuration file mtime changed or previously unknown.")

            if force or changed or self.presets is None:
                log.debug("(Re-)Reading configuration.")
                (
                    preset_names,
                    self.settings,
                    self.default_preset
                ) = get_qjackctl_presets(qjackctl_conf, self.ignore_default)
                self.presets = {name: name.replace('_', ' ')
                                for name in preset_names}
                self.create_menu()

            self._conf_mtime = mtime
        elif self.presets or self.presets is None:
            log.warning("Could not access configuration file.")

            if __debug__ and self.presets:
                log.debug("Removing stored presets from memory.")

            self.presets = {}
            self.settings = {}
            self.default_preset = None
            self.create_menu()

        return True  # keep function scheduled

    def check_alsa_settings(self, preset):
        engine = self.settings[preset]['engine']
        driver = self.settings[preset]['driver']
        if engine['driver'] != 'alsa':
            return True

        dev = driver.get('device')
        if dev and dev not in self.alsainfo.devices:
            log.debug("Device '%s' used by preset '%s' not found.",
                      dev, preset)
            return False

        dev = driver.get('playback')
        if dev and dev not in self.alsainfo.playback_devices:
            log.debug("Playback device '%s' used by preset '%s' not found.",
                      dev, preset)
            return False

        dev = driver.get('capture')
        if dev and dev not in self.alsainfo.capture_devices:
            log.debug("Capture device '%s' used by preset '%s' not found.",
                      dev, preset)
            return False

        return True

    def create_menu(self):
        log.debug("Building menu.")
        self.gui.clear_menu()

        if self.presets:
            if not self.alsainfo:
                log.debug("ALSA device info not available. Filtering disabled.")

            callback = self.activate_preset
            for name, label in sorted(self.presets.items()):
                disabled = self.alsainfo and not self.check_alsa_settings(name)
                self.gui.add_menu_item(callback, label, active=not disabled, data=name)

        else:
            self.gui.add_menu_item(None, "No presets found", active=False)

        self.gui.add_separator()
        self.menu_stop = self.gui.add_menu_item(self.stop_jack_server,
                                                "Stop JACK Server",
                                                icon='stop.png',
                                                active=bool(self.jack_status.get('is_started')))
        self.gui.add_separator()
        self.menu_quit = self.gui.add_menu_item(self.quit, "Quit", icon='quit.png')
        self.gui.menu.show_all()

    def open_menu(self):
        self.gui.on_popup_menu_open()

    def receive_jack_status(self, value, name=None):
        if name == 'is_started':
            if value != self.jack_status.get('is_started'):
                if value:
                    self.gui.set_icon('started.png')
                    log.info("JACK server has started.")
                    self.menu_stop.set_sensitive(True)
                else:
                    self.gui.set_icon('stopped.png')
                    self.tooltext = "JACK server is stopped."
                    log.info(self.tooltext)
                    self.menu_stop.set_sensitive(False)

        self.jack_status[name] = value

        if self.jack_status.get('is_started'):
            try:
                if self.active_preset:
                    label = self.presets.get(self.active_preset,
                                             self.active_preset)
                    self.tooltext = "<b>[%s]</b>\n" % label
                else:
                    self.tooltext = "<i><b>Unknown configuration</b></i>\n"

                self.tooltext += ("%(samplerate)i Hz / %(period)i frames "
                                  "(%(latency)0.1f ms)\n" % self.jack_status)
                self.tooltext += "RT: %s " % (
                    "yes" if self.jack_status.get('is_realtime') else "no")
                self.tooltext += ("load: %(load)i%% xruns: %(xruns)i" %
                                  self.jack_status)
            except KeyError:
                self.tooltext = "No status available."

    def handle_device_change(self, observer=None, device=None, init=False):
        if device:
            dev = device.device_path.split('/')[-1]

        if init or (device.action in ('change', 'remove')
                    and dev.startswith('card')):
            try:
                log.debug("Sound device change signalled. Collecting ALSA "
                          "device info...")
                self.alsainfo = AlsaInfo(deferred=False)
            except Exception as exc:
                log.warn("Could not get ALSA device list: %s", exc)
                self.alsainfo = None

            if device and device.action != 'init':
                self.load_presets(force=True)

    def handle_jackctl_signal(self, *args, signal=None, **kw):
        if signal == 'ServerStarted':
            self.receive_jack_status(True, name='is_started')
        elif signal == 'ServerStopped':
            self.receive_jack_status(False, name='is_started')

    def get_jack_stats(self):
        if self.jackctl and self.jack_status.get('is_started'):
            cb = self.receive_jack_status
            self.jackctl.is_realtime(cb)
            self.jackctl.get_sample_rate(cb)
            self.jackctl.get_period(cb)
            self.jackctl.get_load(cb)
            self.jackctl.get_xruns(cb)
            self.jackctl.get_latency(cb)

        return True  # keep function scheduled

    def tooltip_query(self, widget, x, y, keyboard_mode, tooltip):
        """Set tooltip for the systray icon."""
        if self.jackctl:
            tooltip.set_markup(self.tooltext)
        else:
            tooltip.set_text("No JACK-DBus connection")

        return True

    def activate_default_preset(self):
        if self.default_preset:
            log.debug("Activating default preset '%s'.", self.default_preset)
            self.activate_preset(preset=self.default_preset)
        else:
            log.warn("No default preset set.")

    def activate_preset(self, m_item=None, **kwargs):
        if m_item:
            preset = m_item.data
        else:
            preset = kwargs.get('preset')

        if not preset:
            log.warn("Preset must not be null.")
            return

        settings = self.settings.get(preset)

        if settings:
            self.jackcfg.activate_preset(settings)
            log.info("Activated preset: %s", preset)
            self.stop_jack_server()
            GObject.timeout_add(INTERVAL_RESTART, self.start_jack_server)
            self.active_preset = preset
        else:
            log.error("Unknown preset '%s'. Ignoring it.", preset)

    def start_jack_server(self, *args, **kwargs):
        if self.jackctl and not self.jack_status.get('is_started'):
            log.debug("Starting JACK server...")
            try:
                self.jackctl.start_server()
            except Exception as exc:
                log.error("Could not start JACK server: %s", exc)

    def stop_jack_server(self, *args, **kwargs):
        if self.jackctl and self.jack_status.get('is_started'):
            self.active_preset = None
            log.debug("Stopping JACK server...")

            try:
                self.jackctl.stop_server()
            except Exception as exc:
                log.error("Could not stop JACK server: %s", exc)

    def quit(self, *args):
        log.debug("Exiting main loop.")
        Gtk.main_quit()


def get_dbus_client(bus=None):
    if bus is None:
        bus = dbus.SessionBus()

    obj = bus.get_object(DBUS_NAME, DBUS_PATH)
    return dbus.Interface(obj, DBUS_INTERFACE)


def main(args=None):
    """Main function to be used when called as a script."""
    from dbus.mainloop.glib import DBusGMainLoop

    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument(
        '--version',
        action="version",
        version="%%(prog)s %s" % __version__,
        help="Show program version and exit.")
    ap.add_argument(
        '-a', '--no-alsa-monitor',
        action="store_true",
        help="Disable ALSA device monitoring and filtering.")
    ap.add_argument(
        '-c', '--config',
        metavar='PATH',
        help="Path to configuration file (default: <XDG_CONFIG_HOME>/%s)" % DEFAULT_CONFIG)
    ap.add_argument(
        '-d', '--default',
        action="store_true",
        help="Activate default preset.")
    ap.add_argument(
        '-i', '--ignore-default',
        action="store_true",
        help="Ignore the nameless '(default)' preset if any other presets are stored in the "
             "configuration.")
    ap.add_argument(
        '-v', '--verbose',
        action="store_true",
        help="Be verbose about what the script does.")
    ap.add_argument(
        'preset',
        nargs='?',
        help="Configuration preset to activate on startup.")

    args = ap.parse_args(args if args is not None else sys.argv[1:])

    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO,
                        format="[%(name)s] %(levelname)s: %(message)s")

    # the mainloop needs to be set before creating the session bus instance
    DBusGMainLoop(set_as_default=True)
    bus = dbus.SessionBus()

    try:
        client = get_dbus_client(bus)
        log.debug("JACK-Select DBus service detected.")

        if args.default:
            log.debug("Activating default preset.")
            client.ActivateDefaultPreset()
        elif args.preset:
            log.debug("Activating preset '%s'.", args.preset)
            client.ActivatePreset(args.preset)
        else:
            log.debug("Opening menu...")
            client.OpenMenu()
    except dbus.DBusException as exc:
        log.debug("Exception: %s", exc)
        app = JackSelectApp(bus,
                            config=args.config,
                            monitor_devices=not args.no_alsa_monitor,
                            ignore_default=args.ignore_default)

        if args.default:
            # load default preset when mainloop starts
            GObject.timeout_add(0, app.activate_default_preset)
        elif args.preset:
            # load given preset when mainloop starts
            GObject.timeout_add(0, lambda: app.activate_preset(preset=args.preset))

        try:
            return Gtk.main()
        except KeyboardInterrupt:
            return "Interrupted."


if __name__ == '__main__':
    sys.exit(main() or 0)
