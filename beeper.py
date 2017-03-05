import RPi.GPIO as GPIO
from time import sleep

FREQUENCY = 1000
DUTY_CYCLE = 10
INTERVAL = 0.3
DURATION = 0.05
PIN = 21  # BCM index
BEEPS = 8

def beep(times=BEEPS):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIN, GPIO.OUT)

    p = GPIO.PWM(PIN, FREQUENCY)

    while times > 0:
        p.start(DUTY_CYCLE)
        sleep(DURATION)
        p.stop()
        sleep(INTERVAL)
        times -= 1

    GPIO.cleanup()

if __name__ == "__main__":
    beep()
