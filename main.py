import time
import RPi.GPIO as GPIO
import numpy as np
w = 1
x = 1
REVOLUTION_STEP_NUMBER = 2048


in1 = 15
in2 = 18
en = 14
in3 = 23
in4 = 24
enb = 25
temp1=1

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(en,GPIO.OUT)
GPIO.setup(enb,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.LOW)
p=GPIO.PWM(en,1000)

p.start(100)
p2=GPIO.PWM(enb,1000)

p2.start(100)

GPIO.setwarnings(False)
print("\n")
print("The default speed & direction of motor is HIGH")
print("^c-stop/exit w-forward s-backward d-right a-left l-low m-medium h-high")
print("\n")      
GPIO_PIN_LIST = [4, 17, 27, 22]
   
   
def init_gpio(pinlist):
    """
    Initialize GPIO.
    :param pinlist: GPIO list. Order is important...
    :return: None
    """
    GPIO.setmode(GPIO.BCM)
    for pin in pinlist:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, 0)
   
   
class StepperMotor(object):
    def __init__(self, gpio_pin_list):
        """
        Initialize GPIO and Step Motor status.
        :param gpio_pin_list: GPIO list
        """
        self.gpio_list = gpio_pin_list
        init_gpio(self.gpio_list)
        self.phase = [1, 1, 0, 0]
   
    def get_phase(self):
        """
        Get the phase of the 4 phases Stepper motor.
        :return: phase of step motor
        """
        return self.phase
   
    def rotate_segment(self, direction=True):
        """
        Perform one step.
        :param direction: (Boolean) Clockwise = True | Inverted = False
        :return: None
        """
        if direction:
            self.phase = np.roll(self.phase, 1)
        else:
            self.phase = np.roll(self.phase, -1)
   
        for pin_idx in range(len(self.gpio_list)):
            GPIO.output(self.gpio_list[pin_idx], int(self.phase.astype(int)[pin_idx]))
   
    def rotate(self, direction, degrees=0):
        """
        Perform rotation with direction and angle info.
        :param direction: (Boolean) Clockwise = True | Inverted = False
        :param degrees: angle of rotation
        :return: None
        """
        step_number = int(REVOLUTION_STEP_NUMBER * degrees / 360)
        for i in range(0, step_number):
            degrees = str(degrees)
            print("Turning " + degrees+ " degrees.")
            degrees = float(degrees)
            self.rotate_segment(direction=direction)
            time.sleep(.002)
   
motor = StepperMotor(GPIO_PIN_LIST)
a = 0
d = 0
d2 = 0
initW = 0
a2 = 0
try:
    if __name__ == '__main__':
        while True:
            dg = 40
            dg2 = 40 
            dg3 = 80 / 2
            x = input()
            if x=='l':
                print("low")
                p.ChangeDutyCycle(25)
                p2.ChangeDutyCycle(25)


            elif x=='m':
                print("medium")
                p.ChangeDutyCycle(50)
                p2.ChangeDutyCycle(50)


            elif x=='h':
                print("high")
                p.ChangeDutyCycle(100)
                p2.ChangeDutyCycle(100)
            elif x == "a" and a ==0:
                a2 = 1
                w=0
                d2 = 0
                a +=1
                if initW ==1:
                    dg = 40
                elif d == 1:
                    dg = 80 
                d = 0

                motor.rotate(direction=True, degrees=dg)
                initW = 0
       
                if a == 1:
                    pass
            elif x == "d" and d == 0:

                a2 = 0
                d2 =1
                w= 0

                d +=1
                if initW == 1:
                    dg2 = 40
                elif a == 1:
                    dg2 = 80
                a = 0
                motor.rotate(direction=False, degrees=dg2)
                initW = 0
                if d ==1:
                    pass
            elif x == "w" and w == 0 and a2 == 1:
                GPIO.output(in1,GPIO.HIGH)
                GPIO.output(in2,GPIO.LOW)
                GPIO.output(in3,GPIO.HIGH)
                GPIO.output(in4,GPIO.LOW)
                a = 0
                d = 0
                a2 = 0
                d2 = 0
                w+=1
                initW = 1   
                motor.rotate(direction=False, degrees=dg3)
       
                if w ==1:
                    pass

            elif x == "w" and w == 0 and d2 == 1:
                GPIO.output(in1,GPIO.HIGH)
                GPIO.output(in2,GPIO.LOW)
                GPIO.output(in3,GPIO.HIGH)
                GPIO.output(in4,GPIO.LOW) 
                a = 0
                d = 0
                a2 = 0
                d2 = 0
                w+=1
                initW = 1 
                motor.rotate(direction=True, degrees=dg3)
            elif x == "w":
                GPIO.output(in1,GPIO.HIGH)
                GPIO.output(in2,GPIO.LOW)
                GPIO.output(in3,GPIO.HIGH)
                GPIO.output(in4,GPIO.LOW) 
                if w ==1:
                    pass

            elif x=='s' and w == 0 and d2 ==1:
                motor.rotate(direction=True, degrees=dg3)
                GPIO.output(in1,GPIO.LOW)
                GPIO.output(in2,GPIO.HIGH)
                GPIO.output(in3,GPIO.LOW)
                GPIO.output(in4,GPIO.HIGH)
            elif x=='s' and w == 0 and a2 ==1:
                motor.rotate(direction=False, degrees=dg3)
                GPIO.output(in1,GPIO.LOW)
                GPIO.output(in2,GPIO.HIGH)
                GPIO.output(in3,GPIO.LOW)
                GPIO.output(in4,GPIO.HIGH)
            elif x=='s':
                GPIO.output(in1,GPIO.LOW)
                GPIO.output(in2,GPIO.HIGH)
                GPIO.output(in3,GPIO.LOW)
                GPIO.output(in4,GPIO.HIGH)
            else:
                pass

except KeyboardInterrupt:
    if x == 'w':
        pass
    elif x =="d": 
        motor.rotate(direction=True, degrees=40)


    elif x == "a":
        motor.rotate(direction=False, degrees=40)

    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.LOW)
    GPIO.output(in3,GPIO.LOW)
    GPIO.output(in4,GPIO.LOW)
