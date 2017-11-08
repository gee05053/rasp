import time
from easy_rascar import RasCar

car = RasCar
distance = 17
obstacle = 1
while True :
    current_distance = car.ultraSonicSensor.get_distance()
    print("Distance : " + current_distance)
    if current_distance > distance :
        car.run("F",40)
        print("Obstacle : " + obstacle)
    else :
        car.stop()
        time.sleep(1)
        if obstacle == 1 :
            car.curve_turn("R")
            car.stop()
            time.sleep(1)
            obstacle += 1
            continue
        else :
            car.curve_turn("L")
            car.stop()
            time.sleep(1)
            car.run("F",40,3)
            stop()
            break