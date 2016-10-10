#!/usr/bin/python


# Motor izq 4
# Motor der 5

import time
import maestro as m
s= m.Controller()


while True:
    s.setTarget(4,0)
    s.setTarget(5,0)
    s.setTarget(4,1)
    s.setTarget(5,1)

    time.sleep(3)

    s.setTarget(4,0)
    s.setTarget(5,0)
    s.setTarget(4,-1)
    s.setTarget(5,-1)

    time.sleep(3)

