from gpiozero import DistanceSensor
import time

sensor = DistanceSensor(echo=13, trigger=11, max_distance=2.0)

# Gets the distance in meters.
def getdis():
    distances = []
    for _ in range(9):
        distances.append(sensor.distance)
    distances.sort()
    return distances[4]