#!/usr/bin/env python3

import socket
import sys
import os

serv = "./samsung_ctl"
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

if __name__ == "__main__":
    sys.exit(0) if not os.path.exists(serv) else {}
    sock.connect(serv)
    sock.send(bytes("cyc wifi".encode('utf-8')))
    data = sock.recv(4096)
    print(data.decode('ascii'))
    sock.close()


