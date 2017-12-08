from easy_rascar import RasCarUsingTrackingSensor
import time


def rotates_until_reaches_black_line_point_turn(direction, speed, running_time):
    while True:
        tracking_status = car.trackingSensor.scan()
        print("Turn:", tracking_status)
        if direction == "R" and tracking_status in (
        [1, 1, 0, 0, 1], [1, 1, 0, 1, 1], [1, 0, 0, 1, 1], [1, 0, 1, 1, 1]):
            break
        elif direction == "L" and tracking_status in (
        [1, 0, 0, 1, 1], [1, 1, 0, 1, 1], [1, 1, 0, 0, 1], [1, 1, 1, 0, 1]):
            break
        else:
            car.point_turn(direction, speed, running_time)
            car.stop()
            # gap
            time.sleep(0.1)


def rotates_until_reaches_black_line_swing_turn(direction, speed, running_time):
    while True:
        tracking_status = car.trackingSensor.scan()
        print("Turn:", tracking_status)
        if direction == "R" and tracking_status in (
        [1, 1, 0, 0, 1], [1, 1, 0, 1, 1], [1, 0, 0, 1, 1], [1, 0, 1, 1, 1]):
            break
        elif direction == "L" and tracking_status in (
        [1, 0, 0, 1, 1], [1, 1, 0, 1, 1], [1, 1, 0, 0, 1], [1, 1, 1, 0, 1]):
            break
        else:
            car.swing_turn(direction, speed, running_time)
            car.stop()
            # gap
            time.sleep(0.1)


car = RasCarUsingTrackingSensor(0, 0)

while True:
    tracking_status = car.trackingSensor.scan()
    print(tracking_status)

    if tracking_status == [0, 0, 0, 0, 0]:
        car.run("F", 30, 0.15)
        inner_tracking_status = car.trackingSensor.scan()
        if inner_tracking_status == tracking_status:
            break
        else:
            car.swing_turn("R", 90, 0.3)
            rotates_until_reaches_black_line_swing_turn("R", 90, 0.05)
    elif tracking_status == [1, 0, 0, 1, 1]:
        car.curve_turn("L", 20, 35, 0.05)
    elif tracking_status == [1, 1, 0, 0, 1]:
        car.curve_turn("R", 20, 35, 0.05)
    elif tracking_status == [1, 0, 1, 1, 1]:
        car.curve_turn("L", 20, 26, 0.05)
    elif tracking_status == [1, 1, 1, 0, 1]:
        car.curve_turn("R", 20, 26, 0.05)
    elif tracking_status[4] == 0:
        car.run("F", 30, 0.2)
        car.swing_turn("R", 90, 0.3)
        rotates_until_reaches_black_line_swing_turn("R", 90, 0.05)
    elif tracking_status == [1, 1, 1, 1, 1]:
        car.run("F", 30, 0.6)
        car.point_turn("L", 90, 0.3)
        rotates_until_reaches_black_line_point_turn("L", 90, 0.06)
    elif tracking_status == [0, 0, 0, 1, 1] or tracking_status == [0, 1, 0, 1, 1]:
        car.run("F", 30, 0.2)
        inner_tracking_status = car.trackingSensor.scan()
        if inner_tracking_status == [1, 1, 1, 1, 1]:
            car.swing_turn("L", 90, 0.3)
            rotates_until_reaches_black_line_swing_turn("L", 90, 0.05)
        else:
            continue
    else:
        car.run("F", 30)