#!/usr/bin/python


# Motor izq 4
# Motor der 5

import time
import maestro as m
s= m.Controller()

s.setTarget(4,0)
s.setTarget(5,0)

