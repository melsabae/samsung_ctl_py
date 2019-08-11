#!/usr/bin/env python3

import io
from itertools import chain
from functools import partial as partial_apply


_controls = {
    "cpu": ["silent", "normal", "overclock"]
    , "usb": ["0", "1"]
    , "wifi": ["0", "1"]
    , "bt": ["0", "1"]
}


def _get_next_in_cycle(l: [str], v: str) -> str:
    return l[(l.index(v) + 1) % len(l)]


def _get_file_value(fp: str) -> str:
    return io.open(fp, "r").readline().strip()


def _get_current_value(fp: str, c: str) -> str:
    v = _get_file_value(fp)
    return "{} {}".format(c, v)


def _update_value(fp: str, c: str, v: str) -> bool:
    s = lambda: "set {} {}".format(c, v)
    r = lambda: "set {} {} failed".format(c, v)
    return s() if io.open(fp, "w").write(v) == len(v) else r()


def _cycle_value(fp: str, c: str) -> bool:
    return  _update_value(fp, c, _get_next_in_cycle(_controls[c], _get_file_value(fp)))


def _nullary_nullity(s):
    return "invalid command: {}".format(s)


def _generate_control_action(fp, s):
    ss = str.split(s, " ")

    if "get" == ss[0]:
        return partial_apply(_get_current_value, fp=fp, c=ss[1])

    if "set" == ss[0]:
        return partial_apply(_update_value, fp=fp, c=ss[1], v=ss[2])

    if "cyc" == ss[0]:
        return partial_apply(_cycle_value, fp=fp, c=ss[1])

    return partial_apply(_nullary_nullity, s=s)


def _generate_control_actions(fp, control):
    if control not in _controls:
        return []

    l = chain.from_iterable([
        ["get {}".format(control), "cyc {}".format(control)]
        , map(lambda _: "set {} {}".format(control, _), _controls[control])
    ])

    return map(lambda _: (_, _generate_control_action(fp, _)), l)


def generate_actions(file_paths):
    control_actions = map(lambda _: _generate_control_actions(file_paths[_], _), file_paths)
    return dict(chain.from_iterable(control_actions))

