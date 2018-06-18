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
        "usb_charge": "./usb"
        }

_controls = {
        "performance_level": ["silent", "normal", "overclock"],
        "usb_charge": ["0", "1"],
        }

ux = {
        "cpu": "performance_level",
        "usb": "usb_charge",
        }


def get_file_path(c: str) -> str:
    return _filepaths[ux[c]]


def get_control_values(c: str) -> [str]:
    return _controls[ux[c]]


def get_next_in_cycle(l: [str], c: str) -> str:
    return l[(l.index(c) + 1) % len(l)]


def get_current_value(c: str) -> str:
    return io.open(get_file_path(c), "r").readline().strip()


def update_value(c: str, v: str) -> bool:
    fp = get_file_path(c)
    return io.open(fp, "w").write(v) == len(v)


def cycle_value(c: str) -> bool:
    cv = get_control_values(c)
    curr = get_current_value(c)
    n = get_next_in_cycle(cv, curr)
    return update_value(c, n)

