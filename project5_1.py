from easy_car import RasCar, TrackingSensor
import time

car = RasCar()


def rotates_until_reaches_black_line(direction, speed, running_time):
    while True:
        current_tracking_sensor_status = car.trackingSensor.scan()
        if current_tracking_sensor_status in ([1, 1, 0, 1, 1], [1, 0, 0, 1, 1], [1, 1, 0, 0, 1], [1,0,1,1,1], [1,1,1,0,1]):
            break
        else:
            car.point_turn(direction, speed, running_time)
            #car.stop()
            # gap
            #time.sleep(0.1)

try :
    while True :
        get_tracking = car.trackingSensor.scan()
        print(get_tracking)

        if get_tracking == [1,0,0,1,1] :
            car.curve_turn("L", 25, 27, 0.015)
        elif get_tracking == [1,1,0,0,1] :
            car.curve_turn("R", 25, 27, 0.015)
        elif get_tracking == [1,0,1,1,1] :
            car.curve_turn("L", 15, 17, 0.015)
        elif get_tracking == [1,1,1,0,1] :
            car.curve_turn("R", 15, 17, 0.015)
        else :
            car.run("F", 35)


except KeyboardInterrupt:
    car.stop()