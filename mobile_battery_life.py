#!/usr/bin/env python3

import socket
import sys
import os
import logging

logger = print


serv = "./samsung_ctl"

if __name__ == "__main__":
    for _ in ["set cpu silent", "set bt 0", "set wifi 1", "set usb 0"]:
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.connect(serv)
        #sock.send(bytes("cyc {}".format(_).encode('utf-8')))
        sock.send(bytes(_.encode('utf-8')))
        sock.recv(4096)
        sock.close()

    sys.exit(0)
