from easy_rascar import RasCarUsingTrackingSensor
import RPi.GPIO as GPIO


def rotates_until_reaches_black_line(way_to_turn, direction, speed, running_time):
    while True:
        current_tracking_sensor_status = car.trackingSensor.scan()
        print("Turn:", current_tracking_sensor_status)

        # maybe the car arrives at the finishing line
        if current_tracking_sensor_status == [0, 0, 0, 0, 0]:
            break

        # Turn until reaches black line normally
        if direction == "R" and current_tracking_sensor_status in (
                [1, 1, 0, 0, 1], [1, 1, 0, 1, 1], [1, 0, 0, 1, 1], [1, 0, 1, 1, 1]):
            break
        elif direction == "L" and current_tracking_sensor_status in (
                [1, 0, 0, 1, 1], [1, 1, 0, 1, 1], [1, 1, 0, 0, 1], [1, 1, 1, 0, 1]):
            break
        else:
            if way_to_turn == "swing":
                car.swing_turn(direction, speed, running_time)
            elif way_to_turn == "point":
                car.point_turn(direction, speed, running_time)


car = RasCarUsingTrackingSensor(0, 0)
try:
    while True:
        tracking_status = car.trackingSensor.scan()
        print(tracking_status)

        # Line Tracing
        if tracking_status == [1, 1, 0, 1, 1]:
            car.run("F", 40, -1)
        if tracking_status == [1, 0, 0, 1, 1]:
            car.curve_turn("L", 30, 35, -1)
        elif tracking_status == [1, 1, 0, 0, 1]:
            car.curve_turn("R", 30, 35, -1)
        elif tracking_status == [1, 0, 1, 1, 1]:
            car.curve_turn("L", 30, 50, -1)
        elif tracking_status == [1, 1, 1, 0, 1]:
            car.curve_turn("R", 30, 50, -1)

        # if the car detects 0 at the rightmost sensor
        elif tracking_status[4] == 0:
            car.run("F", 40, 0.4)
            # if the car arrives at the finishing line
            if car.trackingSensor.scan() == [0, 0, 0, 0, 0]:
                break
            else:
                car.swing_turn("R", 90, 0.25)
                rotates_until_reaches_black_line("swing", "R", 70, -1)
        elif tracking_status == [1, 1, 1, 1, 1]:
            car.run("F", 40, 0.4)
            rotates_until_reaches_black_line("point", "L", 45, -1)
        elif tracking_status == [0, 0, 0, 1, 1] or tracking_status == [0, 1, 0, 1, 1]:
            car.run("F", 40, 0.4)
            if car.trackingSensor.scan() == [1, 1, 1, 1, 1]:
                rotates_until_reaches_black_line("swing", "L", 45, -1)
            else:
                continue
        else:
            car.run("F", 20)
except KeyboardInterrupt:
    car.stop()
    GPIO.cleanup()
