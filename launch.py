import math
import time
import krpc

turn_start_altitude = 250
turn_end_altitude = 45000
target_altitude = 150000


class Launch:

    # Set up streams for telemetry

    def __init__(self):
        self.conn = krpc.connect()
        self.vessel = self.conn.space_center.active_vessel
        abort = self.conn.add_stream(getattr, self.vessel.control, 'abort')
        self.add_streams()
        self.pre_launch_setup()
        self.count_down()
        self.stage()
        self.lock_auto_pilot()
        self.do_ascent()

    def add_streams(self):
        self.ut = self.conn.add_stream(getattr, self.conn.space_center, 'ut')
        self.altitude = self.conn.add_stream(
            getattr, self.vessel.flight(), 'mean_altitude')
        self.apoapsis = self.conn.add_stream(
            getattr, self.vessel.orbit, 'apoapsis_altitude')
        self.stage_2_resources = self.vessel.resources_in_decouple_stage(
            stage=2, cumulative=False)
        self.srb_fuel = self.conn.add_stream(
            self.stage_2_resources.amount, 'SolidFuel')

    # Pre-launch setup

    def pre_launch_setup(self):
        self.vessel.control.sas = False
        self.vessel.control.rcs = False
        self.vessel.control.throttle = 1.0

    # Countdown...

    def count_down(self):
        print('3...')
        time.sleep(1)
        print('2...')
        time.sleep(1)
        print('1...')
        time.sleep(1)
        print('Launch!')

    # Activate the first stage
    def stage(self):
        self.vessel.control.activate_next_stage()

    def lock_auto_pilot(self):
        self.vessel.auto_pilot.engage()
        self.vessel.auto_pilot.target_pitch_and_heading(90, 90)

    def do_ascent(self):
        # Main ascent loop
        srbs_separated = False
        turn_angle = 0
        while True:
            # Gravity turn
            if self.altitude() > turn_start_altitude and self.altitude() < turn_end_altitude:
                frac = ((self.altitude() - turn_start_altitude) /
                        (turn_end_altitude - turn_start_altitude))
                new_turn_angle = frac * 90
                if abs(new_turn_angle - turn_angle) > 0.5:
                    turn_angle = new_turn_angle
                    self.vessel.auto_pilot.target_pitch_and_heading(
                        90-turn_angle, 90)

            # Separate SRBs when finished
            if not srbs_separated:
                if self.srb_fuel() < 0.1:
                    self.vessel.control.activate_next_stage()
                    srbs_separated = True
                    print('SRBs separated')

            # Decrease throttle when approaching target apoapsis
            if self.apoapsis() > target_altitude*0.9:
                print('Approaching target apoapsis')
                break


doLaunch = Launch()
