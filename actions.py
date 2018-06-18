#!/usr/bin/env python3

import io
from sys import argv, exc_info


_filepaths = {
        "performance_level": "/sys/devices/platform/samsung/performance_level",
        "usb_charge": "/sys/devices/platform/samsung/usb_charge",
        }

_controls = {
        "performance_level": ["silent", "normal", "overclock"],
        "usb_charge": ["0", "1"],
        }

_ux = {
        "cpu": "performance_level",
        "usb": "usb_charge"
        }


def get_file_path(c: str) -> str:
    return _filepaths[c]


def get_control_values(c: str) -> [str]:
    return _controls[c]


def get_next_in_cycle(l: [str], c: str) -> str:
    return l[(l.index(c) + 1) % len(l)] if c in l else None


def get_current_value(c: str) -> str:
    return io.open(get_file_path(c), "r").readline().strip()


def write_new_value(fp: str, v: str) -> bool:
    return io.open(fp, "w").write(v) == len(v)


def cycle_value(c: str) -> bool:
    fp = get_file_path(c)
    cv = get_control_values(c)
    curr = get_current_value(c)
    n = get_next_in_cycle(cv, curr)
    return write_new_value(fp, n)


#def main(i: str):
#    r = False
#    try:
#        r = cycle_value(i)
#    except:
#        pass
#    finally:
#        if r:
#            print("{} updated to {}".format(i, get_current_value(i)))
#
#        if not r:
#            print("{} unchanged (permissions error?)".format(i))


if __name__ == "__main__":
    if len(argv) > 1 and argv[1] in _ux:
        main(_ux[argv[1]])
    else:
        print("usage: {} {}".format(argv[0], list(_ux)))
