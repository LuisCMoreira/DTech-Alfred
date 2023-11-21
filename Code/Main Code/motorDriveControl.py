import RPi.GPIO as GPIO
import time
import threading

class MotorController:
    def __init__(self, motorTag, encoder_pins, motor_pins):
        self.motorTag = motorTag   
        self.encoder_pins = encoder_pins
        self.motor_pins = motor_pins
        self.encoder_lock = threading.Lock()
        self.encoderCount = 0
        self.lastEncoderCount = 0
        self.lastEcnCountTime = 1000*(time.time())
        self.rotSpeed = 0
        self.encodToRot = 400 # encoder counts per end shaft rotation
        self.motorFactor = 25/(100) # max duty cicle for max endshaft rpm
        self.speedCorrectFactor = 0
        self.setRotSpeed = 0
        self.dutyCycle=0
        
                
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.encoder_pins, GPIO.IN)
        GPIO.setup(self.motor_pins, GPIO.OUT)
        self.pwm = GPIO.PWM(self.motor_pins[0], 1000)
        self.pwm.start(0)
        GPIO.output(self.motor_pins[1], GPIO.LOW)
        GPIO.output(self.motor_pins[2], GPIO.LOW)
        
        encoder_pin_0 = self.encoder_pins[0]
        encoder_pin_1 = self.encoder_pins[1]

        GPIO.add_event_detect(encoder_pin_0, GPIO.RISING, callback=self.encoder_callback)

        #GPIO.add_event_detect(encoder_pin_1, GPIO.RISING, callback=self.encoder_callback)
 

    def encoder_callback(self, channel):
        with self.encoder_lock:
            if GPIO.input(self.motor_pins[2]) and not GPIO.input(self.motor_pins[1]):
                self.encoderCount += 1
            elif GPIO.input(self.motor_pins[1]) and not GPIO.input(self.motor_pins[2]):
                self.encoderCount -= 1

            if abs(self.encoderCount - self.lastEncoderCount) > 16 and 1000*time.time()>self.lastEcnCountTime:
                self.rotSpeed = (60*1000) * ((self.encoderCount - self.lastEncoderCount) / self.encodToRot) / (
                        ((1000*time.time()-self.lastEcnCountTime))
                )


                self.lastEcnCountTime = 1000*(time.time())
                self.lastEncoderCount = self.encoderCount
                

                if (int(self.rotSpeed)>int(self.setRotSpeed)) and self.speedCorrectFactor>-75:
                    self.speedCorrectFactor =self.speedCorrectFactor - 1
    
                if (int(self.rotSpeed)<int(self.setRotSpeed)) and self.speedCorrectFactor<75:
                    self.speedCorrectFactor =self.speedCorrectFactor + 1   
                
        
                self.dutyCycle=abs(self.setRotSpeed*self.motorFactor+self.speedCorrectFactor)
                
                if self.dutyCycle>100:
                    self.dutyCycle=100
                elif self.dutyCycle<0:
                    self.dutyCycle=0  
                
                    
                self.pwm.ChangeDutyCycle(self.dutyCycle)
                
                print(f"##### Motor: {self.motorTag} Set Rotation Speed: {self.setRotSpeed} Rotation Speed: {self.rotSpeed} Duty Cycle: {self.dutyCycle} Correction:{self.speedCorrectFactor} Encoder Count: {self.encoderCount}")
               
            
            print(f"Motor: {self.motorTag} Set Rotation Speed: {self.setRotSpeed} Rotation Speed: {self.rotSpeed} Duty Cycle: {self.dutyCycle} Correction:{self.speedCorrectFactor} Encoder Count: {self.encoderCount}")
            
                      

    def motor_drive(self, setRotSpeed):
    
        self.speedCorrectFactor=0
        
        self.setRotSpeed=setRotSpeed
        
        
        self.dutyCycle=abs(self.setRotSpeed*self.motorFactor+self.speedCorrectFactor)
        
        if self.dutyCycle>100:
          self.dutyCycle=100
        elif self.dutyCycle<0:
          self.dutyCycle=0  
        
        #print(self.dutyCycle)
        
        if setRotSpeed == 0:
            GPIO.output(self.motor_pins[1], GPIO.LOW)
            GPIO.output(self.motor_pins[2], GPIO.LOW)
            self.pwm.ChangeDutyCycle(0)
        elif setRotSpeed > 0:
            GPIO.output(self.motor_pins[1], GPIO.LOW)
            GPIO.output(self.motor_pins[2], GPIO.HIGH)
            self.pwm.ChangeDutyCycle(self.dutyCycle)   
        elif setRotSpeed < 0:
            GPIO.output(self.motor_pins[1], GPIO.HIGH)
            GPIO.output(self.motor_pins[2], GPIO.LOW)
            self.pwm.ChangeDutyCycle(self.dutyCycle)

    def cleanup(self):
        GPIO.cleanup()

