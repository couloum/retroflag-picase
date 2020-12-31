import RPi.GPIO as GPIO
import os
import time
from multiprocessing import Process

#initialize pins
fanPin = 21 #pin 40

# Temperatures at which the fan start and stop
# Use different temperatures to avoid frequent start/stop
startThreshold = 55
stopThreshold = 45

fanFlag = GPIO.HIGH

#initialize GPIO settings
def init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(fanPin, GPIO.OUT)
    startFan()
    GPIO.setwarnings(False)

def startFan():
    global fanFlag
    fanFlag = GPIO.HIGH
    print "Starting Fan"
    GPIO.output(fanPin, fanFlag)

def stopFan():
    global fanFlag
    fanFlag = GPIO.LOW
    print "Stopping Fan"
    GPIO.output(fanPin, fanFlag)

#waits for user to hold button up to 1 second before issuing poweroff command
def checkTemperature():
    while True:
        with open("/sys/class/thermal/thermal_zone0/temp") as f:
            temp = float(f.read().strip()) / 1000

        print "Temperature = %.2f / Fan Status = %s / start: %d / stop: %d" % \
                (temp, fanFlag, startThreshold, stopThreshold)
        if temp >= startThreshold and fanFlag != GPIO.HIGH:
            startFan()
        elif temp < stopThreshold and fanFlag != GPIO.LOW:
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
