from easy_rascar import Rascar, TrackingSensor
import time

car = Rascar()

try :
    while True :
        get_tracking = car.TrackingSensor.scan()
        print(get_tracking)

        # line tracing
        if get_tracking == [1,0,0,1,1] :
            car.curve_turn("R",15,15,-1)
        elif get_tracking == [1,1,0,0,1] :
            car.curve_turn("L",15,15,-1)

        # right turn or stop
        elif get_tracking == [1,1,0,0,0] or get_tracking == [0,0,0,0,0]:
            car.run("F", 35, 0.5)
            get_tracking2 = car.TrackingSensor.scan()
            if get_tracking2 == [0,0,0,0,0] : # stop
                car.stop()
            else : # right turn
                car.swing_turn("R", 90, 0.25)
                while True : # [1,1,0,1,1] 될 때 까지 회전
                    get_tracking3 = car.TrackingSensor.scan()
                    if get_tracking3 == [1,1,0,1,1] or get_tracking3 == [1,0,0,1,1] or get_tracking3 == [1,1,0,0,1]:
                        break
                    else :
                        car.swing_turn("R", 90, 0,1)

        #left turn or go straight
        elif get_tracking == [0,0,0,1,1] :
            car.run("F", 35, 0.5)
            get_tracking2 = car.TrackingSensor.scan()
            if get_tracking2 == [1,1,0,1,1] : # go straight
                continue
            else : # left turn
                car.swing_turn("L", 90, 0.25) # 45도 왼쪽 회전
                while True :
                    get_tracking3 = car.TrackingSensor.scan()
                    if get_tracking3 == [1,1,0,1,1] or get_tracking3 == [1,0,0,1,1] or get_tracking3 == [1,1,0,0,1]:
                        break
                    else :
                        car.swing_turn("L", 90, 0.1)
        else :
            car.run("F",35)


except KeyboardInterrupt :
    car.stop()