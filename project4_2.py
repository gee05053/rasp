from easy_rascar import RasCar, TrackingSensor, UltraSonicSensor
import time

car = RasCar()
dis = 15
obstacle = 1

try :
    while True :
        get_tracking = car.trackingSensor.scan()
        get_distance = car.ultraSonicSensor.get_distance()
        print(get_tracking)
        print("Distance :", get_distance)
        if get_distance > dis : 
            if get_tracking == [1,0,1,1,1] or get_tracking == [1,0,0,1,1]:
                car.curve_turn("L")
            elif get_tracking == [0,0,1,1,1] or get_tracking == [0,1,1,1,1]:
                car.curve_turn2("L")
            elif get_tracking == [1,1,1,1,0] or get_tracking == [1,1,1,0,1] or get_tracking == [1,1,0,0,1]:
                car.curve_turn("R")
            elif get_tracking == [1,1,1,0,0] :
                car.curve_turn2("R")
            elif get_tracking == [1,0,0,0,1] or get_tracking == [0,0,0,0,1] or get_tracking == [0,0,0,1,1]:
                car.curve_turn2("R")
            elif get_tracking == [1,1,1,1,1] :
                car.curve_turn2("L")
            elif get_tracking == [0,0,0,0,0] :
                car.stop()
                break 
            else :
                car.run("F", 40)
            print("Obstacle :", obstacle)
        else :
            obstacle += 1
            car.stop()
            time.sleep(0.1)
            car.point_turn("R")
            car.run("F",50,1.4)
            car.stop()
            time.sleep(0.1)
            car.point_turn("L")
            car.run("F",20, 1)

except KeyboardInterrupt :
    car.stop() 
