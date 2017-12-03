from easy_rascar import RasCar, TrackingSensor
import time

car = RasCar()


def rotates_until_reaches_black_line(direction, speed, running_time):
    while True:
        current_tracking_sensor_status = car.trackingSensor.scan()
        if direction == "R" and current_tracking_sensor_status in ([1, 1, 0, 1, 1], [1,0,0,1,1], [1,0,1,1,1]):
            break
        if direction == "L" and current_tracking_sensor_status in ([1,1,0,1,1], [1,1,0,0,1], [1,1,1,0,1]) :
            break
        else:
            car.point_turn(direction, speed, running_time)
            car.stop()
            # gap
            time.sleep(0.13)

try :
    while True :
        get_tracking = car.trackingSensor.scan()
        print(get_tracking)

        if get_tracking == [1,0,0,1,1] :
            car.curve_turn("L", 10, 14, 0.015)
        elif get_tracking == [1,1,0,0,1] :
            car.curve_turn("R", 10, 14, 0.015)
        elif get_tracking == [1,0,1,1,1] :
            car.curve_turn("L", 10, 12, 0.015)
        elif get_tracking == [1,1,1,0,1] :
            car.curve_turn("R", 10, 12, 0.015)
        elif get_tracking == [1,1,0,0,0] or get_tracking == [1,1,0,1,0] :
            car.run("F", 35, 0.7)
            car.point_turn("R", 90, 0.2)
            rotates_until_reaches_black_line("R", 90, 0.07)
        elif get_tracking == [1,1,1,1,1] :
            car.run("F", 20, 0.7)
            car.point_turn("R", 90, 0.2)
            rotates_until_reaches_black_line("R", 90, 0.07)
        elif get_tracking == [0,0,0,1,1] :
            car.run("F", 30, 0.7)
            car.point_turn("L", 90, 0.2)
            rotates_until_reaches_black_line("L", 90, 0.07)
        else :
            car.run("F", 15)


except KeyboardInterrupt:
    car.stop()
