from gpiozero import PWMLED

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

vibpin = PWMLED(12)

# Vibrates based off distance. 
def vibrate(d):
    if d <= 2.0 and d >= 0.0:
        intensity = 100 - (d / 2 * 100)
        vibpin.value(intensity/100)
    else:
        vibpin.value(0)