import RPi.GPIO as GPIO
from time import sleep


def remap(x, oMin, oMax, nMin, nMax):

    # range check
    if oMin == oMax:
        print("Warning: Zero input range")
        return None

    if nMin == nMax:
        print("Warning: Zero output range")
        return None

    # check reversed input range
    reverseInput = False
    oldMin = min(oMin, oMax)
    oldMax = max(oMin, oMax)
    if not oldMin == oMin:
        reverseInput = True

    # check reversed output range
    reverseOutput = False
    newMin = min(nMin, nMax)
    newMax = max(nMin, nMax)
    if not newMin == nMin:
        reverseOutput = True

    portion = (x-oldMin)*(newMax-newMin)/(oldMax-oldMin)
    if reverseInput:
        portion = (oldMax-x)*(newMax-newMin)/(oldMax-oldMin)

    result = portion + newMin
    if reverseOutput:
        result = newMax - portion

    return result


DIR_PIN = 11
STEP_PIN = 13

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(DIR_PIN, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(STEP_PIN, GPIO.OUT, initial=GPIO.LOW)

maxSteps = 200
topSpeed = 0.001
pastAngle = 0
err = True

try:
    while True:
        angles = int(input("Insert angle (0-360): "))
        newAngle = round(remap(angles, 0, 360, 0, maxSteps)
                         )
        while pastAngle != newAngle:
            if pastAngle < newAngle:
                GPIO.output(DIR_PIN, GPIO.LOW)
                pastAngle = + 1

            if (pastAngle >= newAngle):
                GPIO.output(DIR_PIN, GPIO.HIGH)
                pastAngle = - 1

            GPIO.output(STEP_PIN, GPIO.HIGH)
            sleep(topSpeed)
            GPIO.output(STEP_PIN, GPIO.LOW)
            sleep(topSpeed)

            print(f'Past Angle = {pastAngle} | New Angle {newAngle} |\n')

        pastAngle = newAngle
        print(f"Current angle = {angles}")
        sleep(1)

except KeyboardInterrupt:
    sleep(1)
    print('Fuck')
