import pyttsx3

engine = pyttsx3.init()

engine.setProperty('volume', 1.0)
engine.setProperty('rate', 150)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[11].id)

# Speaks the person, who they are, and how far away they are.
def speech(person, des, distance):
    engine.say(f"{person}, your {des}, is {distance} meters away.")
    engine.runAndWait()
def speech2():
    engine.say("Greetings my friend")
    engine.runAndWait()


speech2()