#!/usr/bin/python

from maestro import Controller

class ControllerJus(Controller):
    
    leftDir = 1
    rightDir = 1

    def __init__(self, leftDir, rightDir):
        Controller.__init__(self)
        self.leftDir = leftDir
        self.rightDir = rightDir

    
    def goAhead(self, cLeft, cRight):
        targetLeft = 1*self.leftDir
        targetRight = 1*self.rightDir
        self.applyMove(targetLeft, targetRight, cLeft, cRight)


    def goBack(self, cLeft, cRight):
        targetLeft = -1*self.leftDir
        targetRight = -1*self.rightDir
        self.applyMove(targetLeft, targetRight, cLeft, cRight)

    def stop(self, cLeft, cRight):
        targetLeft = 0*self.leftDir
        targetRight = 0*self.rightDir
        self.applyMove(targetLeft, targetRight, cLeft, cRight)

    def rotateLeft(self, cLeft, cRight):
        targetLeft = -1*self.leftDir
        targetRight = 1*self.rightDir
        self.applyMove(targetLeft, targetRight, cLeft, cRight)

    def rotateRight(self, cLeft, cRight):
        targetLeft = 1*self.leftDir
        targetRight = -1*self.rightDir
        self.applyMove(targetLeft, targetRight, cLeft, cRight)

    def applyMove(self, left, right, cLeft, cRight):
        targetLeft = left
        targetRight = right
        # if Min is defined and Target is below, force to Min
        if self.Mins[cLeft] > 0 and targetLeft < self.Mins[cLeft]:
            targetLeft = self.Mins[cLeft]
        # if Max is defined and Target is above, force to Max
        if self.Maxs[cLeft] > 0 and targetLeft > self.Maxs[cLeft]:
            targetLeft = self.Maxs[cLeft]
        # if Min is defined and Target is below, force to Min
        if self.Mins[cRight] > 0 and targetRight < self.Mins[cRight]:
            targetRight = self.Mins[cRight]
        # if Max is defined and Target is above, force to Max
        if self.Maxs[cRight] > 0 and targetRight > self.Maxs[cRight]:
            targetRight = self.Maxs[cRight]
        lsbLeft = targetLeft & 0x7f #7 bits for least significant byte
        msbLeft = (targetLeft >> 7) & 0x7f #shift 7 and take next 7 bits for msb
        lsbRight = targetRight & 0x7f #7 bits for least significant byte
        msbRight = (targetRight >> 7) & 0x7f #shift 7 and take next 7 bits for msb
        # Send Pololu intro, device number, command, channel, and target lsb/msb
        cmdLeft = self.PololuCmd + chr(0x04) + chr(cLeft) + chr(lsbLeft) + chr(msbLeft)
        cmdRight = self.PololuCmd + chr(0x04) + chr(cRight) + chr(lsbRight) + chr(msbRight)                          
        self.usb.write(cmdLeft)
        self.usb.write(cmdRight)
        # Record Target value
        self.Targets[cLeft] = targetLeft
        self.Targets[cRight] = targetRight
    
        
    # Set speed of channel
    # Speed is measured as 0.25microseconds/10milliseconds
    # For the standard 1ms pulse width change to move a servo between extremes, a speed
    # of 1 will take 1 minute, and a speed of 60 would take 1 second.
    # Speed of 0 is unrestricted.
    def setSpeed(self, chan, speed):
        lsb = speed & 0x7f #7 bits for least significant byte
        msb = (speed >> 7) & 0x7f #shift 7 and take next 7 bits for msb
        # Send Pololu intro, device number, command, channel, speed lsb, speed msb
        cmd = self.PololuCmd + chr(0x07) + chr(chan) + chr(lsb) + chr(msb)
        self.usb.write(cmd)

    # Set acceleration of channel
    # This provide soft starts and finishes when servo moves to target position.
    # Valid values are from 0 to 255. 0=unrestricted, 1 is slowest start.
    # A value of 1 will take the servo about 3s to move between 1ms to 2ms range.
    def setAccel(self, chan, accel):
        lsb = accel & 0x7f #7 bits for least significant byte
        msb = (accel >> 7) & 0x7f #shift 7 and take next 7 bits for msb
        # Send Pololu intro, device number, command, channel, accel lsb, accel msb
        cmd = self.PololuCmd + chr(0x09) + chr(chan) + chr(lsb) + chr(msb)
        self.usb.write(cmd)
    
    # Get the current position of the device on the specified channel
    # The result is returned in a measure of quarter-microseconds, which mirrors
    # the Target parameter of setTarget.
    # This is not reading the true servo position, but the last target position sent
    # to the servo. If the Speed is set to below the top speed of the servo, then
    # the position result will align well with the acutal servo position, assuming
    # it is not stalled or slowed.
    def getPosition(self, chan):
        cmd = self.PololuCmd + chr(0x10) + chr(chan)
        self.usb.write(cmd)
        lsb = ord(self.usb.read())
        msb = ord(self.usb.read())
        return (msb << 8) + lsb

    # Test to see if a servo has reached its target position.  This only provides
    # useful results if the Speed parameter is set slower than the maximum speed of
    # the servo. 
    # ***Note if target position goes outside of Maestro's allowable range for the
    # channel, then the target can never be reached, so it will appear to allows be
    # moving to the target.  See setRange comment.
    def isMoving(self, chan):
        if self.Targets[chan] > 0:
            if self.getPosition(chan) <> self.Targets[chan]:
                return True
        return False
    
    # Have all servo outputs reached their targets? This is useful only if Speed and/or
    # Acceleration have been set on one or more of the channels. Returns True or False.
    def getMovingState(self):
        cmd = self.PololuCmd + chr(0x13)
        self.usb.write(cmd)
        if self.usb.read() == chr(0):
            return False
        else:
            return True

    # Run a Maestro Script subroutine in the currently active script. Scripts can
    # have multiple subroutines, which get numbered sequentially from 0 on up. Code your
    # Maestro subroutine to either infinitely loop, or just end (return is not valid).
    def runScriptSub(self, subNumber):
        cmd = self.PololuCmd + chr(0x27) + chr(subNumber)
        # can pass a param with command 0x28
        # cmd = self.PololuCmd + chr(0x28) + chr(subNumber) + chr(lsb) + chr(msb)
        self.usb.write(cmd)

    # Stop the current Maestro Script
    def stopScript(self):
        cmd = self.PololuCmd + chr(0x24)
        self.usb.write(cmd)

