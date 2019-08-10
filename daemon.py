#!/usr/bin/env python3


import socket
import sys
import io
import os
import logging
import signal
from functools import partial as p
import actions as act
from itertools import chain


def get_paths(l):
    if any([
        False
        , len(l) is 0 or "#" is l[0]
        , ":" not in l
    ]):
        return ("/dev/null", "/dev/null")

    s = str.split(l, ":")
    ss = list(map(str.strip, s))
    ln = "{}".format(ss[0])
    lt = "{}".format(ss[1])
    return ln, lt


def remove_link(n):
    os.unlink(n) if os.path.exists(n) else {}


def setup_link(t):
    remove_link(t[0])
    os.symlink(t[1], t[0])


def setup_links(lf):
    fc = map(str.strip, io.open(lf, 'r', encoding="utf-8").readlines())
    lts = list(filter(lambda _: _ != ("/dev/null", "/dev/null"), map(get_paths, fc)))
    list(map(setup_link, lts))
    list(map(lambda _: logger(_[0]), lts))
    return lts


def get_action(m, i):
    return m[i] if i in m else lambda: "NACK"


def sig_handler(signum, frame):
    global _sock
    global _serv
    global logger

    logger("{} {}".format("received signal", signum))
    global_cleanup()
    sys.exit(0)


def global_setup():
    global _links
    global _symlinks

    _symlinks = setup_links(_links)


def global_cleanup():
    global _serv
    global _sock
    global _symlinks

    _sock.close()
    os.unlink(_serv) if os.path.exists(_serv) else {}
    list(map(lambda _: remove_link(_[0]), _symlinks))


def main():
    global _sock
    global _serv
    global _am

    global_setup()

    os.unlink(_serv) if os.path.exists(_serv) else {}

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    prev_mask = os.umask(0o000)  # set permissions for socket
    _sock.bind(_serv)
    os.umask(prev_mask)  # restore permissions

    _sock.listen()

    while True:
        conn, _ = _sock.accept()
        try:
            data = conn.recv(4096)
            c = tuple(data.decode('utf-8').split())
            res = get_action(_am, c)()
            conn.send(bytes(res.encode('utf-8')))
            logger("recv: {}, send: {}".format(repr(c), repr(res)))
        finally:
            conn.close()




_sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
_serv = "./samsung_ctl"
_links = "./links"
_symlinks = []
logger = print


"""
Command format: {get, set, cyc} {_ in ux} ["set" parameter]
"""
_am = {
        k:v for k, v in chain(
            ((("get", _), p(act.get_current_value, c=_)) for _ in act.ux)
            , ((("cyc", _), p(act.cycle_value, c=_)) for _ in act.ux)
            , ((("set", _, __), p(act.update_value, c=_, v=__)) for _ in act.ux for __ in act.get_control_values(_))
        )
}

if __name__ == "__main__":
    main()

