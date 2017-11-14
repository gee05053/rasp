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
                car.curve_turn("L",30,15,-1) 
            elif get_tracking == [0,0,1,1,1]:
                car.curve_turn("L",28,28,-1)
            elif get_tracking == [1,1,1,1,1] or get_tracking == [0,1,1,1,1] or get_tracking == [1,0,0,0,0]:
                car.curve_turn("L",0.5,95,-1)
            elif get_tracking == [1,1,1,1,0] or get_tracking == [1,1,1,0,1] or get_tracking == [1,1,0,0,1]:
                car.curve_turn("R")
            elif get_tracking == [1,0,0,0,1] or get_tracking == [0,0,0,0,1] or get_tracking == [0,0,0,1,1] or get_tracking == [1,1,1,0,0] \
                    or get_tracking == [1,1,0,0,0]:
                car.curve_turn("R",15,25,-1)
            elif get_tracking == [0,0,0,0,0] :
                car.stop()
                break
            else :
                car.run("F", 25) 
            print("Obstacle :", obstacle)
        else :
            obstacle += 1
            car.stop()
            time.sleep(0.5)
            car.point_turn("R",90,0.3)
            car.run("F",40,1.7)
            car.stop()
            time.sleep(0.5)
            car.point_turn("L",90,0.6)
            car.stop()
            time.sleep(0.5)
            while not(0 in car.trackingSensor.scan()) :
                car.run("F", 20)
            car.run("F", 30, 0.4)
            while not(0 in car.trackingSensor.scan()) :
                car.point_turn("R",50,-1)

except KeyboardInterrupt :
    car.stop()
