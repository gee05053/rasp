from easy_rascar import RasCar, TrackingSensor, UltraSonicSensor
import time

car = RasCar()
dis = 20
obstacle = 1

try :
    while True :
        get_tracking = car.trackingSensor.scan()
        get_distance = car.ultraSonicSensor.get_distance()
        print(get_tracking)
        print("Distance :", get_distance)
        if get_distance > dis : 
            if get_tracking == [0,1,1,1,1] or get_tracking == [0,0,1,1,1] or get_tracking == [1,0,1,1,1] or get_tracking == [1,0,0,1,1]: 
                car.curve_turn("L")
            elif get_tracking == [1,1,1,1,0] or get_tracking == [1,1,1,0,0] or get_tracking == [1,1,1,0,1] or get_tracking == [1,1,0,0,1]:
                car.curve_turn("R")
            elif get_tracking == [0,0,0,0,0] :
                car.stop()
                break 
            else :
                car.run("F", 35)
            print("Obstacle :", obstacle)
        else :
            obstacle += 1
            car.stop()
            time.sleep(1)
            car.swing_turn("R")
            car.stop()
            time.sleep(1)
            car.run("F",35,1)
            car.swing_turn("L")
            car.stop()
            time.sleep(1)
            car.run("F", 35)
            car.stop()
            time.sleep(1)
            car.curve_turn("L")
            car.stop()
            time.sleep(1)
            car.run("F", 35, 0.5)
except KeyboardInterrupt :
    car.stop() 
