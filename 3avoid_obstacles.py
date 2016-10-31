#!/usr/bin/python

import time
import maestroJus as m

# Crear objeto MicroMaestro
s= m.ControllerJus(-1,1)

# Asignacion de canales
sharp = 0
servo_izq = 4
servo_dcho = 5

# Distancia de evitacion (600 choque, 0 sin obstaculo)
distance= 200

# Tiempos de movimiento y pausa para estabilizacion de lectura
avance = 0.5
turning = 0.75
stopped= 0.5

s.setAccel(4,1)

# Lecturas de distancia a obstaculo antes de arrancar
iter=1
while (1):
	pos_min = s.getPosition(0)
	pos_max = s.getPosition(0)
	pos=0.5*(pos_min+pos_max)
	print "ITERACION ",iter
	iter = iter + 1
	print "Distancia (600-0)=",pos
	if pos > distance:
		print "Me paro pq hay obstaculo"
                s.stop(4,5)
		time.sleep(turning)
		print "Rotando para evitar obstaculo"
		s.rotateLeft(4,5)
        	time.sleep(turning)
                s.stop(4,5)
		time.sleep(stopped)

		pos_min = s.getPosition(0)
		pos_max = s.getPosition(0)
        	pos=0.5*(pos_min+pos_max)
		print "Distancia tras evitar=",pos
	elif pos > distance:
		break
	else:
		s.goAhead(4,5)
	print ""
	time.sleep(avance)
