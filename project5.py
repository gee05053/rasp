from easy_rascar import RasCar, TrackingSensor
import time

car = RasCar()

try:
    while True:
        get_tracking = car.trackingSensor.scan()
        print(get_tracking)

        # line tracing
        if get_tracking == [1, 0, 0, 1, 1]:
            car.curve_turn("L", 25, 27, 0.02)
        elif get_tracking == [1, 0, 1, 1, 1]:
            car.curve_turn("L", 30, 32, 0.02)
        elif get_tracking == [1, 1, 0, 0, 1]:
            car.curve_turn("R", 25, 27, 0.02)
        elif get_tracking == [1, 1, 1, 0, 1]:
            car.curve_turn("R", 30, 32, 0.02)

        # right turn or stop
        elif get_tracking == [1, 1, 0, 0, 0] or get_tracking == [1, 0, 0, 0, 0] or get_tracking == [0, 0, 0, 0, 0]:
            car.run("F", 35, 0.6)
            get_tracking2 = car.trackingSensor.scan()
            if get_tracking2 == [0, 0, 0, 0, 0]:  # stop
                car.stop()
                break
            else:  # right turn
                car.swing_turn("R", 90, 0.2)
                while True:  # [1,1,0,1,1] 될 때 까지 회전
                    get_tracking3 = car.trackingSensor.scan()
                    if get_tracking3 == [1, 1, 0, 1, 1] or get_tracking3 == [1, 0, 0, 1, 1] or get_tracking3 == [1, 1,
                                                                                                                 0, 0,
                                                                                                                 1]:
                        break
                    else:
                        car.swing_turn("R", 90, 0.1)
                        car.stop()
                        time.sleep(0.1)

        # left turn or go straight
        elif get_tracking == [0, 0, 0, 1, 1] or get_tracking == [0, 0, 0, 0, 1]:
            car.run("F", 35, 0.5)
            get_tracking2 = car.trackingSensor.scan()
            # If there is no line
            if get_tracking2 == [1, 1, 1, 1, 1]:
                car.swing_turn("L", 90, 0.3)  # 45도 왼쪽 회전
                while True:
                    get_tracking3 = car.trackingSensor.scan()
                    if get_tracking3 == [1, 1, 0, 1, 1] or get_tracking3 == [1, 0, 0, 1, 1] or get_tracking3 == [1, 1,
                                                                                                                 0, 0,
                                                                                                                 1]:
                        break
                    else:
                        car.swing_turn("L", 90, 0.1)
                        car.stop()
                        time.sleep(0.1)
            else:  # left turn
                continue
        elif get_tracking == [1, 1, 1, 1, 1]:
            car.swing_turn("R", 90, 0.3)
            while True:
                get_tracking2 = car.trackingSensor.scan()
                if get_tracking2 == [1, 1, 0, 1, 1] or get_tracking2 == [1, 1, 0, 0, 1] or get_tracking2 == [1, 0, 0, 1,
                                                                                                             1]:
                    break
                else:
                    car.swing_turn("R", 90, 0.1)
                    car.stop()
                    time.sleep(0.1)
        else:
            car.run("F", 35)


except KeyboardInterrupt:
    car.stop()
