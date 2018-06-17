#!/usr/bin/env python3

import os
import select

pipe_name = "samsung_ctl"

os.mkfifo(pipe_name) if not os.path.exists(pipe_name) else ()

while True:
    with open(pipe_name, "r") as pipe:
        dat = pipe.readline()
        #convert = list(map(lambda _: _.strip(), dat))
        convert = dat.strip()
        print(dat)
