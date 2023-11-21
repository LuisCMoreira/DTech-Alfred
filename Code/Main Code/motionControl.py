import motorDriveControl
import time
import math
       
#Example usage:
motorRT = motorDriveControl.MotorController(motorTag="motorRT", encoder_pins=(18, 23), motor_pins=(12, 13, 6))
motorLF = motorDriveControl.MotorController(motorTag="motorLF", encoder_pins=(27, 22), motor_pins=(26, 21, 20))





#max linear speed is 0,34 m/s

#wheel to rotation
wheelDia=0.065
axisDist=0.25
rotToLinear= 2*math.pi*(wheelDia/2) # one rotation * this var = meters moved

def linearToRot(linearSpeed):
    speed=round(((linearSpeed*60)/rotToLinear),2)
    return speed

def getMotorVariables():
    global motorLFDuty, motorRTDuty
    motorLFDuty=motorLF.dutyCycle
    motorRTDuty=motorRT.dutyCycle
    
    return motorLFDuty, motorRTDuty

def moveL(linearSpeed):
    print(linearToRot(linearSpeed))
    motorRT.motor_drive(linearToRot(linearSpeed))
    motorLF.motor_drive(linearToRot(linearSpeed))
    

    
def moveSTOP():    
    motorRT.motor_drive(0)
    motorLF.motor_drive(0)
    


def moveRT(linearSpeed):
    motorRT.motor_drive(linearToRot(linearSpeed))
    motorLF.motor_drive(-linearToRot(linearSpeed))
    

    
 


forTest=False

try:
    while forTest:
        moveL(0.16)
        print(motorRT.rotSpeed)
        time.sleep(10)
        moveSTOP()
        time.sleep(5)
        moveL(0.34)
        time.sleep(5)
        moveSTOP()
        time.sleep(2)
        moveRT(0.34)
        time.sleep(2)
        moveRT(-0.34)
        time.sleep(2)
        moveSTOP()
        time.sleep(2)

except KeyboardInterrupt:
    motorRT.cleanup()
    motorLF.cleanup()

