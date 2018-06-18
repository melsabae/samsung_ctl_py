#!/usr/bin/env python3


import socket
import sys
import os
import logging
import signal
from functools import partial as p
import actions as act


logger = print

ga = list((("get", _), p(act.get_current_value, c=_)) for _ in act.ux)
ca = list((("cyc", _), p(act.cycle_value, c=_)) for _ in act.ux)
sa = [(("set", _, __), p(act.update_value, l=_, v=__)) for _ in act.ux for __ in act.get_control_values(_)]
am = { k: v for (k,v) in ga + ca + sa }

#list(map(lambda _: print(_, am[_]), am))
#print('\n\n', ga[0], ga[0][1]())
#sys.exit(0)



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

    sock.bind(serv)
    sock.listen()

    while True:
        conn, _ = sock.accept()

        """
        Command format: {get, set, cyc} {_ in ux} ["set" parameter]
        """

        try:
            data = conn.recv(4096)

            # convert byte data into string-based command set
            # split the words into strings
            # then convert to a tuple, which makes a key in the action map

            t = data.decode('uft-8')  # ascii might be choice
            c = tuple( t.split() )

            logger("{} {}".format("received", repr(t)))

            if c in am:
                # run the command, sending back the result
                # along the lines of
                # res = am[c]()
                # conn.send( bytes( res.encode( 'utf-8' )))
                pass

            if c not in am:
                conn.send(b'NACK')
        finally:
            conn.close()


sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
if __name__ == "__main__":
    main()

