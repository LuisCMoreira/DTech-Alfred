import RPi.GPIO as GPIO
import time
import threading

try:
  GPIO.cleanup()
except KeyboardInterrupt:
  pass



# Set the GPIO mode to BCM numbering
GPIO.setmode(GPIO.BCM)

# Define the GPIO pins for the encoders
encoder1_pins = (18, 23)
encoder2_pins = (27, 22)

# Initialize pulse counts
encoder1_count = 0
encoder2_count = 0

# Set PWM Duty Cycle
PWM1DutyCycle=50
PWM2DutyCycle=50

# Initialize GPIO for encoders
GPIO.setup(encoder1_pins + encoder2_pins, GPIO.IN)

GPIO.setup(21, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)
GPIO.setup(26, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)


# Callback function to handle encoder events for Encoder 1
def encoder1_callback(channel):
    global encoder1_count
    if GPIO.input(20) and not GPIO.input(21):
      encoder1_count += 1
      print(f"Encoder 1 Count: {encoder1_count}")
    elif GPIO.input(21) and not GPIO.input(20):
      encoder1_count -= 1
      print(f"Encoder 1 Count: {encoder1_count}")
    

def encoder2_callback(channel):
    global encoder2_count
    if GPIO.input(6) and not GPIO.input(13):
      encoder2_count += 1
      print(f"Encoder 2 Count: {encoder2_count}")
    elif GPIO.input(13) and not GPIO.input(6):
      encoder2_count -= 1
      print(f"Encoder 2 Count: {encoder2_count}")
      
      

# Add interrupt event detection for both encoder channels
GPIO.add_event_detect(encoder1_pins[0], GPIO.RISING, callback=encoder1_callback)

GPIO.add_event_detect(encoder2_pins[0], GPIO.RISING, callback=encoder2_callback)




# Set pin 20 to output and set it to True (High)
GPIO.output(21, GPIO.LOW)
GPIO.output(20, GPIO.HIGH)

# Set pin 6 to output and set it to True (High)
GPIO.output(13, GPIO.LOW)
GPIO.output(6, GPIO.HIGH)


# Set pin 26 to PWM mode with a 75% duty cycle

pwmLF = GPIO.PWM(26, 1000)  # 1000 Hz frequency
pwmLF.start(PWM1DutyCycle)  # 75% duty cycle


# Set pin 12 to PWM mode with a 75% duty cycle

pwmRT = GPIO.PWM(12, 1000)  # 1000 Hz frequency
pwmRT.start(PWM2DutyCycle)  # 75% duty cycle



# Keep the program running for some time to maintain the settings
#try:
#    time.sleep(2)  # Run for 10 seconds
#except KeyboardInterrupt:
#    pass

PWM1DutyCycle_=PWM1DutyCycle

time.sleep(0.1) 
      
while encoder1_count<360:
  # Keep the program running for some time to maintain the settings
  try:
    if encoder2_count>encoder1_count+5:
        if PWM1DutyCycle_>PWM1DutyCycle-10:
          PWM1DutyCycle_=PWM1DutyCycle_-1
    
    if encoder2_count<encoder1_count-5:
        if PWM1DutyCycle_<PWM1DutyCycle+10:
          PWM1DutyCycle_=PWM1DutyCycle_+1
    
        
    pwmLF.ChangeDutyCycle(PWM1DutyCycle_)
    
    if encoder1_count>150:
        pwmRT.ChangeDutyCycle(11)
        pwmLF.ChangeDutyCycle(11)
        PWM1DutyCycle=11
        PWM1DutyCycle_=11
    
    time.sleep(0.01)  # Run for 10 seconds
  except KeyboardInterrupt:
    pass



pwmLF.stop()
pwmRT.stop()

time.sleep(2)


PWM1DutyCycle=50
PWM2DutyCycle=50

# Reverse

GPIO.output(20, GPIO.LOW)
# Set pin 21 to output and set it to True (High)

GPIO.output(21, GPIO.HIGH)


GPIO.output(6, GPIO.LOW)
# Set pin 13 to output and set it to True (High)

GPIO.output(13, GPIO.HIGH)



# Set pin 26 to PWM mode with a 75% duty cycle

pwmLF = GPIO.PWM(26, 1000)  # 1000 Hz frequency
pwmLF.start(PWM1DutyCycle)  # 75% duty cycle


# Set pin 12 to PWM mode with a 75% duty cycle

pwmRT = GPIO.PWM(12, 1000)  # 1000 Hz frequency
pwmRT.start(PWM2DutyCycle)  # 75% duty cycle


# Keep the program running for some time to maintain the settings
#try:
#    time.sleep(2)  # Run for 10 seconds
#except KeyboardInterrupt:

#    pass


encoder2_count = encoder1_count
    
PWM1DutyCycle_=PWM1DutyCycle

time.sleep(0.1) 
    
while encoder1_count>0:
  # Keep the program running for some time to maintain the settings
  try:
    if encoder2_count<encoder1_count-5:
        if PWM1DutyCycle_>PWM1DutyCycle-10:
          PWM1DutyCycle_=PWM1DutyCycle_-1
          
    if encoder2_count>encoder1_count+5:
        if PWM1DutyCycle_<PWM1DutyCycle+10:
          PWM1DutyCycle_=PWM1DutyCycle_+1
    
        
    pwmLF.ChangeDutyCycle(PWM1DutyCycle_)
    
    if encoder1_count<150:
        pwmRT.ChangeDutyCycle(11)
        pwmLF.ChangeDutyCycle(11)
        PWM1DutyCycle=11
        PWM1DutyCycle_=11
        
    
    time.sleep(0.01)  # Run for 10 seconds
    
     # Run for 10 seconds
  except KeyboardInterrupt:
    pass




# Cleanup and reset GPIO settings
pwmLF.stop()
pwmRT.stop()
GPIO.cleanup()
