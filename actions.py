#!/usr/bin/env python3

import io
from itertools import chain
from sys import argv, exc_info
from functools import partial as p


_controls = {
        "cpu": ["silent", "normal", "overclock"],
        "usb": ["0", "1"],
        "wifi": ["on", "off"],
        "bt": ["on", "off"],
        }


def nullary_nullity():
    pass


def _generate_control_action(fp, s):
    ss = str.split(s, " ")

    if "get" == ss[0]:
        return p(get_current_value, c=fp)

    if "set" == ss[0]:
        return p(update_value, c=fp, v=ss[2])

    if "cyc" == ss[0]:
        return p(cycle_value, c=fp)

    return nullary_nullity


def _generate_control_actions(fp, control):
    l = chain.from_iterable([
        ["get {}".format(control), "cyc {}".format(control)]
        , map(lambda _: "set {} {}".format(control, _), _controls[control])
    ])

    return map(lambda _: (_, _generate_control_action(fp, _)), l)


def generate_actions(links):
    # TODO: turn links into a map (or be a sane person and make a map as an argument??)
    control_actions = map(lambda _: _generate_control_actions(_[0], _[0]), links)
    return dict(chain.from_iterable(control_actions))


def _get_next_in_cycle(l: [str], c: str) -> str:
    return l[(l.index(c) + 1) % len(l)]


def get_control_values(c: str) -> [str]:
    return _controls[c]


def get_current_value(c: str) -> str:
    # TODO: for controls that do not have files or cannot find
    #  push this function's decisions into a new function that returns the proper action
    #  and keep the return as a string
    return io.open(c, "r").readline().strip()


def update_value(c: str, v: str) -> bool:
    # TODO: for controls that do not have files or cannot find
    #  push this function's decisions into a new function that returns the proper action
    #  and keep the return as a string
    return v if io.open(c, "w").write(v) == len(v) else repr(False)


def cycle_value(c: str) -> bool:
    return  update_value(c, _get_next_in_cycle(get_control_values(c), get_current_value(c)))

