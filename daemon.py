#!/usr/bin/env python3


import socket
import sys
import os
import logging
import signal
import actions as sa

logger = print

tal = list(
        (("set", _, __, sa.get_file_path(_)), lambda: sa.update_value(_, __)) for _ in sa.ux for __ in sa.get_control_values(_)
        )
ga = list(zip([("get", _) for _ in sa.ux], [lambda: sa.get_current_value(_) for _ in sa.ux]))
print(ga[0][0], repr(ga[0][1]()))
sys.exit(0)


ga = list(zip([("get", _) for _ in sa.ux], [lambda: sa.get_current_value(_) for _ in sa.ux]))
ca = list(zip([("cyc", _) for _ in sa.ux], [lambda: sa.cycle_value(_) for _ in sa.ux]))
sa = [(("set", _, __), lambda: sa.update_value(_, __)) for _ in sa.ux for __ in sa.get_control_values(_)]
am = { k: v for (k,v) in ga + ca + sa }


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

