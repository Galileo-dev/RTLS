import numpy as np
import matplotlib
import turtle
import krpc


def abort():
    aborting = True
    control_abort_throttle = False
    e = 2.71828
    conn = krpc.connect()
    vessel = conn.space_center.active_vessel
    vertical_speed = conn.add_stream(
        getattr, vessel.flight(
            vessel.orbit.body.reference_frame), 'vertical_speed'
    )

    while aborting:
        idealThrottle = 1/(1+e**(vertical_speed()))
        # if idealThrottle > 0.7:
        #     control_abort_throttle = True
        # if control_abort_throttle:
        vessel.control.throttle = idealThrottle
        # if vertical_speed() > 0:
        #     aborting = False
        print(idealThrottle)


abort()
