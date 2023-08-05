# -*- coding: utf-8 -*-
"""Read JACK presets and their settings from QjackCtl's configuration file."""

import configparser
import logging


log = logging.getLogger(__name__)
PARAM_MAPPING = {
    'driver': ('engine', 'driver'),
    'realtime': ('engine', 'realtime'),
    'priority': ('engine', 'realtime-priority'),
    'verbose': ('engine', 'verbose'),
    'timeout': ('engine', 'client-timeout'),
    'portmax': ('engine', 'port-max'),
    'servername': ('engine', 'name'),
    'slavedrivers': ('engine', 'slave-drivers'),
    'chan': ('driver', ('inchannels', 'outchannels')),
    'clocksource': 'clock-source',
    'frames': 'period',
    'indevice': 'capture',
    'inlatency': 'input-latency',
    'interface': 'device',
    'mididriver': 'midi-driver',
    'outdevice': 'playback',
    'outlatency': 'output-latency',
    'periods': 'nperiods',
    'samplerate': 'rate',
    'selfconnectmode': 'self-connect-mode',
    # 'snoop': '???'
}
VALUE_MAPPING = {
    'dither': {
        '0': b'n',
        '1': b'r',
        '2': b's',
        '3': b't',
    },
    'clock-source': {
        'c': 0,
        'h': 1,
        's': 2,
    },
    'self-connect-mode': {
        '0': b' ',
        '1': b'e',
        '2': b'E',
        '3': b'a',
        '4': b'A',
    }
}
DEFAULT_PRESET = '(default)'


def get_qjackctl_presets(qjackctl_conf, ignore_default=False):
    config = configparser.ConfigParser()
    config.optionxform = lambda option: option
    config.read(qjackctl_conf)

    preset_names = set()
    settings = {}

    if 'Settings' in config:
        for name in sorted(config['Settings']):
            try:
                preset_name, param = name.split('\\', 1)
            except ValueError:
                # The default (nameless) preset was saved.
                # It uses settings keys without a preset name prefix.
                param = name
                preset_name = DEFAULT_PRESET

            preset_names.add(preset_name)
            param = param.lower()
            value = config.get('Settings', name)
            param = PARAM_MAPPING.get(param, param)

            if isinstance(param, tuple):
                component, param = param
            else:
                component = 'driver'

            if preset_name not in settings:
                settings[preset_name] = {}

            if component not in settings[preset_name]:
                settings[preset_name][component] = {}

            if not isinstance(param, (tuple, list)):
                param = (param,)

            for p in param:
                if p in VALUE_MAPPING:
                    value = VALUE_MAPPING[p].get(value, value)
                if value == 'false':
                    value = False
                elif value == 'true':
                    value = True
                elif value == '':
                    value = None
                else:
                    try:
                        value = int(value)
                    except (TypeError, ValueError):
                        pass

                settings[preset_name][component][p] = value

    if (ignore_default and DEFAULT_PRESET in settings and len(settings) > 1):
        del settings[DEFAULT_PRESET]

        if DEFAULT_PRESET in preset_names:
            preset_names.remove(DEFAULT_PRESET)

    default_preset = config.get('Presets', 'DefPreset', fallback=None)

    if default_preset not in preset_names:
        default_preset = None

    if not default_preset and DEFAULT_PRESET in preset_names:
        default_preset = DEFAULT_PRESET

    return list(preset_names), settings, default_preset


def _test():
    from xdg import BaseDirectory as xdgbase

    qjackctl_conf = xdgbase.load_first_config('rncbc.org/QjackCtl.conf')

    if qjackctl_conf:
        presets, _, default = get_qjackctl_presets(qjackctl_conf, True)
        for preset in sorted(presets):
            print(preset, "*" if preset == default else '')


if __name__ == '__main__':
    _test()
