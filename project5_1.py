from easy_rascar import RasCar, TrackingSensor
import time


def rotates_until_reaches_black_line(direction, speed, running_time):
    while True:
        current_tracking_sensor_status = car.trackingSensor.scan()
        print("Turn:", current_tracking_sensor_status)
        if direction == "R" and current_tracking_sensor_status in ([1,1,0,0,1], [1,1,0,1,1], [1,0,0,1,1], [1,0,1,1,1]):
            break
        elif direction == "L" and current_tracking_sensor_status in ([1,0,0,1,1], [1,1,0,1,1], [1,1,0,0,1], [1,1,1,0,1]) :
            break
        else:
            car.point_turn(direction, speed, running_time)
            car.stop()
            # gap
            time.sleep(0.1)


car = RasCar()

try :
    while True :
        get_tracking = car.trackingSensor.scan()
        print(get_tracking)

        if get_tracking == [1,0,0,1,1] :
            car.curve_turn("L", 10, 28, 0.05)
        elif get_tracking == [1,1,0,0,1] :
            car.curve_turn("R", 10, 28, 0.05)
        elif get_tracking == [1,0,1,1,1] :
            car.curve_turn("L", 10, 20, 0.05)
        elif get_tracking == [1,1,1,0,1] :
            car.curve_turn("R", 10, 20, 0.05)
        elif get_tracking[4] == 0  :
            car.run("F", 30, 0.5)
            car.point_turn("R", 40, 0.2)
            rotates_until_reaches_black_line("R", 70, 0.07)
        elif get_tracking == [1,1,1,1,1] :
            car.run("F", 30, 0.45)
            car.point_turn("L", 40, 0.2)
            rotates_until_reaches_black_line("R", 70, 0.07)
        elif get_tracking == [0,0,0,1,1] or get_tracking == [0,1,0,1,1] :
            car.run("F", 30, 0.43)
            car.point_turn("L", 40, 0.2)
            rotates_until_reaches_black_line("L", 70, 0.07)
        else :
            car.run("F", 10)


except KeyboardInterrupt:
    car.stop()
