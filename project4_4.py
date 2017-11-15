from easy_rascar import RasCar, TrackingSensor, UltraSonicSensor
import time

car = RasCar()
dis = 14.5
obstacle = 0

try :
    while True :
        get_tracking = car.trackingSensor.scan()
        get_distance = car.ultraSonicSensor.get_distance()
        print(get_tracking)
        print("Distance :", get_distance)
        if get_distance > dis :
            if get_tracking == [1,0,1,1,1] or get_tracking == [1,0,0,1,1]:
                car.curve_turn("L",15,17,-1)
            elif get_tracking == [0,0,1,1,1]:
                car.curve_turn("L",18,28,-1)
            elif get_tracking == [1,1,1,1,1] or get_tracking == [0,1,1,1,1] or get_tracking == [1,0,0,0,0]:
                car.curve_turn("L",0.5,95,-1)
            elif get_tracking == [1,1,1,1,0] or get_tracking == [1,1,1,0,1] or get_tracking == [1,1,0,0,1]:
                car.curve_turn("R",15,15,-1)
            elif get_tracking == [1,0,0,0,1] or get_tracking == [0,0,0,0,1] or get_tracking == [0,0,0,1,1] or get_tracking == [1,1,1,0,0] \
                    or get_tracking == [1,1,0,0,0]:
                car.curve_turn("R",15,25,-1)
            elif get_tracking == [0,0,0,0,0] :
                car.stop()
                break
            else :
                car.run("F", 30)
            print("Obstacle :", obstacle)
        else :
            obstacle += 1
            if obstacle == 1 :
                car.point_turn("R",90,0.26)
                car.run("F",40,0.9)
                car.point_turn("L",90,0.52)
            else :
                car.point_turn("R",90,0.26)
                car.run("F",40,0.9)
                car.point_turn("L",90,0.6)
            car.stop()
            time.sleep(0.1)
            while car.trackingSensor.scan().count(0) < 2 :
                car.run("F", 20)
            car.run("F", 20, 0.3)
            while car.trackingSensor.scan().count(0) < 2 :
                car.point_turn("R",40,-1)

except KeyboardInterrupt :
    car.stop()
