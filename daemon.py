#!/usr/bin/env python3


import socket
import sys
import io
import os
import logging
import signal
import actions as act


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


def get_control_file_paths(lf):
    fc = map(str.strip, io.open(lf, 'r', encoding="utf-8").readlines())
    lts = list(filter(lambda _: _ != ("/dev/null", "/dev/null"), map(get_paths, fc)))
    return dict(lts)


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
    global _paths
    global _am

    syms = get_control_file_paths(_paths)
    _am = act.generate_actions(syms)

    # this lists every known control to this program, which may be useful in generating scripts/GUIs
    list(map(print, _am))



def global_cleanup():
    global _serv
    global _sock

    _sock.close()
    os.unlink(_serv) if os.path.exists(_serv) else {}


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
            c = ' '.join(data.decode('utf-8').split())
            res = get_action(_am, c)()
            conn.send(bytes(res.encode('utf-8')))
            logger("recv: {}, send: {}".format(repr(c), repr(res)))
        finally:
            conn.close()




_sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
_serv = "./samsung_ctl"
_paths = "./paths"
logger = print
_am = {}
_file_paths = {}

if __name__ == "__main__":
    main()

