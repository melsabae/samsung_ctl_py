#!/usr/bin/env python3

import socket
import sys
import os
import logging

logger = print

serv = "./samsung_ctl"
os.unlink(serv) if os.path.exists(serv) else {}

logger("{}".format("creating socket"))
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
logger("{}".format("binding socket"))
sock.bind(serv)
sock.listen()

if __name__ == "__main__":
    while True:
        logger("waiting on connection")
        conn, client = sock.accept()

        try:
            logger ("{} {}".format("connection from", client))
            while True:
                data = conn.recv(4096)

                if len(data):
                    t = data.decode('ascii')
                    logger("{} {}".format("received", t))
                else:
                    break
        finally:
            conn.close()
