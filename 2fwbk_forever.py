#!/usr/bin/python

import time
import maestro as m
s= m.Controller()

# Motor izq salida 4
servo_izq=4
# Motor der salida 5
servo_der=5

while True:
    s.setTarget(servo_izq,1)
    s.setTarget(servo_der,1)

    time.sleep(3)

    s.setTarget(servo_izq,0)
    s.setTarget(servo_der,0)
    
    # Espera minima de 0.4 para que coja el cambio de giro
    time.sleep(0.4)

    s.setTarget(servo_izq,-1)
    s.setTarget(servo_der,-1)
    
    time.sleep(3)

    s.setTarget(servo_izq,0)
    s.setTarget(servo_der,0)

    time.sleep(0.4)

