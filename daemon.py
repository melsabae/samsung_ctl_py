#!/usr/bin/env python3


import socket
import sys
import os
import logging
import signal
from functools import partial as p
import actions as act
from itertools import chain


def global_cleanup():
    global _serv
    global _sock

    _sock.close()
    os.unlink(_serv) if os.path.exists(_serv) else {}


def get_action(m, i):
    return m[i] if i in m else lambda: "NACK"


def sig_handler(signum, frame):
    global _sock
    global _serv
    global logger

    logger("{} {}".format("received signal", signum))
    global_cleanup()
    sys.exit(0)


def main():
    global _sock
    global _serv
    global _am

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

