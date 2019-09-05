#!/usr/bin/env python3

import socket
import sys
import os
import logging

logger = print


serv = "./samsung_ctl"

if __name__ == "__main__":
    for _ in ["set cpu overclock", "set bt 1", "set wifi 1", "set usb 1"]:
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.connect(serv)
        #sock.send(bytes("cyc {}".format(_).encode('utf-8')))
        sock.send(bytes(_.encode('utf-8')))
        sock.recv(4096)
        sock.close()

    sys.exit(0)
