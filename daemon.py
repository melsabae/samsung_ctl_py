#!/usr/bin/env python3


import socket
import sys
import os
import logging
import signal
from functools import partial as p
import actions as act
from itertools import chain


logger = print


"""
Command format: {get, set, cyc} {_ in ux} ["set" parameter]
"""
am = {
        k:v for (k, v) in chain(
            ((("get", _), p(act.get_current_value, c=_)) for _ in act.ux)
            , ((("cyc", _), p(act.cycle_value, c=_)) for _ in act.ux)
            , ((("set", _, __), p(act.update_value, c=_, v=__)) for _ in act.ux for __ in act.get_control_values(_))
        )
}


def get_action(i):
    return am[i] if i in am else lambda: "NACK"


def sig_handler(signum, frame):
    global sock
    sock.close()
    logger("{} {}".format("received signal", signum))
    sys.exit(0)


def main():
    global sock
    global am

    serv = "./samsung_ctl"
    os.unlink(serv) if os.path.exists(serv) else {}

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    prev_mask = os.umask(0o000) # set permissions for socket
    sock.bind(serv)
    os.umask(prev_mask)

    sock.listen()

    while True:
        conn, _ = sock.accept()
        try:
            data = conn.recv(4096)
            c = tuple(data.decode('utf-8').split())
            res = get_action(c)()
            conn.send(bytes(res.encode('utf-8')))
            logger("recv: {}, send: {}".format(repr(c), repr(res)))
        finally:
            conn.close()


sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
if __name__ == "__main__":
    main()

