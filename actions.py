#!/usr/bin/env python3

import io
from sys import argv, exc_info


"""
All functions defined herein operate by contract
"""


_filepaths = {
        #"performance_level": "/sys/devices/platform/samsung/performance_level",
        #"usb_charge": "/sys/devices/platform/samsung/usb_charge",
        "performance_level": "./cpu",
        "usb_charge": "./usb",
        "wifi": "./wifi",
        "bluetooth": "./bt",
        }

_controls = {
        "performance_level": ["silent", "normal", "overclock"],
        "usb_charge": ["0", "1"],
        "wifi": ["on", "off"],
        "bluetooth": ["on", "off"],
        }

ux = {
        "cpu": "performance_level",
        "usb": "usb_charge",
        "wifi": "wifi",
        "bt": "bluetooth",
        }


def _get_file_path(c: str) -> str:
    return _filepaths[ux[c]]


def _get_next_in_cycle(l: [str], c: str) -> str:
    return l[(l.index(c) + 1) % len(l)]


def get_control_values(c: str) -> [str]:
    return _controls[ux[c]]


def get_current_value(c: str) -> str:
    # TODO: for controls that do not have files or cannot find
    #  push this function's decisions into a new function that returns the proper action
    #  and keep the return as a string
    return io.open(_get_file_path(c), "r").readline().strip()


def update_value(c: str, v: str) -> bool:
    # TODO: for controls that do not have files or cannot find
    #  push this function's decisions into a new function that returns the proper action
    #  and keep the return as a string
    return v if io.open(_get_file_path(c), "w").write(v) == len(v) else repr(False)


def cycle_value(c: str) -> bool:
    return  update_value(c, _get_next_in_cycle(get_control_values(c), get_current_value(c)))

