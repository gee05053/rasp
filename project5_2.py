from easy_rascar import RasCarUsingTrackingSensor, TrackingSensor
import time


def rotates_until_reaches_black_line_point_turn(direction, speed, running_time):
    while True:
        car.point_turn(direction, speed, running_time)
        current_tracking_sensor_status = car.trackingSensor.scan()
        print("Turn:", current_tracking_sensor_status)
        if direction == "R" and current_tracking_sensor_status in ([1,1,0,0,1], [1,1,0,1,1], [1,0,0,1,1], [1,0,1,1,1]):
            break
        elif direction == "L" and current_tracking_sensor_status in ([1,0,0,1,1], [1,1,0,1,1], [1,1,0,0,1], [1,1,1,0,1]) :
            break
        #else:
            #car.point_turn(direction, speed, running_time)
            #car.stop()
            # gap
            #time.sleep(0.1)

def rotates_until_reaches_black_line_swing_turn(direction, speed, running_time):
    while True:
        current_tracking_sensor_status = car.trackingSensor.scan()
        print("Turn:", current_tracking_sensor_status)
        if direction == "R" and current_tracking_sensor_status in ([1,1,0,0,1], [1,1,0,1,1], [1,0,0,1,1], [1,0,1,1,1]):
            break
        elif direction == "L" and current_tracking_sensor_status in ([1,0,0,1,1], [1,1,0,1,1], [1,1,0,0,1], [1,1,1,0,1]) :
            break
        else:
            car.swing_turn(direction, speed, running_time)
            #car.stop()
            # gap
            #time.sleep(0.1)


car = RasCarUsingTrackingSensor(0,0)

try :
    while True :
        get_tracking = car.trackingSensor.scan()
        print(get_tracking)

        #if get_tracking == [0,0,0,0,0] :
        #    car.run("F", 30, 0.17)
        #    tracking = car.trackingSensor.scan()
        #    if tracking == get_tracking :
        #        break
        #    else :
        #        rotates_until_reaches_black_line_swing_turn("R", 50, -1)
        if get_tracking == [1,0,0,1,1] :
            car.curve_turn("L", 30, 50)
        elif get_tracking == [1,1,0,0,1] :
            car.curve_turn("R", 30, 50)
        elif get_tracking == [1,0,1,1,1] :
            car.curve_turn("L", 30, 36)
        elif get_tracking == [1,1,1,0,1] :
            car.curve_turn("R", 30, 36)
        elif get_tracking[4] == 0  :
            car.run("F", 30, 0.25)
            car.swing_turn("R", 90, 0.27)
            rotates_until_reaches_black_line_swing_turn("R", 45, -1)
        elif get_tracking == [1,1,1,1,1] :
            car.run("F", 30, 0.6)
            rotates_until_reaches_black_line_point_turn("L", 47, -1)
        elif get_tracking == [0,0,0,1,1] or get_tracking == [0,1,0,1,1] :
            car.run("F", 30, 0.2)
            tracking = car.trackingSensor.scan()
            if tracking == [1,1,1,1,1]:
                rotates_until_reaches_black_line_swing_turn("L", 55, -1)
            else :
                continue
        else :
            car.run("F", 40)


except KeyboardInterrupt:
    car.stop()
