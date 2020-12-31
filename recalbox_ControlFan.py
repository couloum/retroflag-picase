import RPi.GPIO as GPIO
import os
import time
from multiprocessing import Process

#initialize pins
fanPin = 21 #pin 40

fanFlag = GPIO.HIGH

#initialize GPIO settings
def init():
    global fanFlag
    global fanPin
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(fanPin, GPIO.OUT)
    startFan()
    GPIO.setwarnings(False)

def startFan():
    global fanFlag
    global fanPin
    fanFlag = GPIO.HIGH
    print "Starting Fan"
    GPIO.output(fanPin, fanFlag)

def stopFan():
    global fanFlag
    global fanPin
    fanFlag = GPIO.LOW
    print "Stopping Fan"
    GPIO.output(fanPin, fanFlag)

#waits for user to hold button up to 1 second before issuing poweroff command
def checkTemperature():
    global fanFlag
    while True:
        with open("/sys/class/thermal/thermal_zone0/temp") as f:
            temp = float(f.read().strip()) / 1000

        print "Temperature = %.2f / Fan Status = %s" % (temp, fanFlag)
        if temp >= 50 and fanFlag != GPIO.HIGH:
            startFan()
        elif temp <= 45 and fanFlag != GPIO.LOW:
            stopFan()

        time.sleep(5)



if __name__ == "__main__":
    print "Starting ControlFan"
    init()
    time.sleep(5)
    tempProcess = Process(target = checkTemperature)
    tempProcess.start()
    tempProcess.join()
    GPIO.cleanup()
