import RPi.GPIO as GPIO
from time import sleep

INTERVAL = 0.3
DURATION = 0.5
PIN = 21  # BCM index
BEEPS = 8

def beep(times=BEEPS):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIN, GPIO.OUT)

    while times > 0:
        GPIO.output(PIN, True)
        sleep(DURATION)
        GPIO.output(PIN, False)
        sleep(INTERVAL)
        times -= 1

    GPIO.cleanup()

if __name__ == "__main__":
    beep()
