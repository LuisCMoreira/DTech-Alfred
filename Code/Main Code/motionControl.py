import motorDriveControl
import time
       
#Example usage:
motorRT = motorDriveControl.MotorController(motorTag="motorRT", encoder_pins=(18, 23), motor_pins=(12, 13, 6))
motorLF = motorDriveControl.MotorController(motorTag="motorLF", encoder_pins=(27, 22), motor_pins=(26, 21, 20))

def moveL(speed):
    motorRT.motor_drive(speed)
    motorLF.motor_drive(speed)
    
def moveSTOP():    
    motorRT.motor_drive(0)
    motorLF.motor_drive(0)

def moveRT(speed):
    motorRT.motor_drive(speed)
    motorLF.motor_drive(-speed)

try:
    while True:
        moveL(50)
        print(motorRT.rotSpeed)
        time.sleep(10)
        moveSTOP()
        time.sleep(5)
        moveL(100)
        time.sleep(5)
        moveSTOP()
        time.sleep(2)
        moveRT(100)
        time.sleep(2)
        moveRT(-100)
        time.sleep(2)
        moveSTOP()
        time.sleep(2)

except KeyboardInterrupt:
    motorRT.cleanup()
    motorLF.cleanup()

