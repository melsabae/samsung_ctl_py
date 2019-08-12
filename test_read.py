#!/usr/bin/env python3

import socket
import sys
import os

serv = "./samsung_ctl"

if __name__ == "__main__":
    sys.exit(0) if not os.path.exists(serv) else {}

    for _ in ["cpu", "usb", "wifi", "bt", "commands", "controls"]:
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.connect(serv)

        sock.send(bytes("get {}".format(_).encode('utf-8')))
        data = sock.recv(4096)
        sock.close()

        print("{}: {}".format(_, data.decode('ascii')))

    sys.exit(0)

