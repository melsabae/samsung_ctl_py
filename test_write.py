#!/usr/bin/env python3

import socket
import sys
import os
import logging

logger = print


serv = "./samsung_ctl"
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

if __name__ == "__main__":
    sock.connect(serv)
    #sock.send(bytes("get cpu".encode('utf-8')))
    #sock.send(bytes("set cpu overclock".encode('utf-8')))
    #sock.send(bytes("cyc cpu".encode('utf-8')))
    sock.send(bytes("cyc usb".encode('utf-8')))
