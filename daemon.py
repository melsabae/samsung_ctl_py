#!/usr/bin/env python3


import socket
import sys
import os
import logging
import signal


logger = print


def sig_handler(signum, frame):
    global sock
    sock.close()
    logger("{} {}".format("received signal", signum))
    sys.exit(0)


def main():
    global sock

    serv = "./samsung_ctl"
    os.unlink(serv) if os.path.exists(serv) else {}

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    sock.bind(serv)
    sock.listen()

    while True:
        conn, _ = sock.accept()

        try:
            data = conn.recv(4096)
            t = data.decode('ascii')

            if len(data):
                logger("{} {}".format("received", repr(t)))
                if t == "req":
                    conn.send(b'ACK')
            else:
                break
        finally:
            conn.close()


sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
if __name__ == "__main__":
    main()

