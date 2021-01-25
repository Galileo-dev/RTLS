import numpy as np
import math
import time


class test_suicide_burn_controller:
    def __init__(self, realism_overhaul, conn):

        self.engine_limit = 0
        self.vessel_height = 1.0471018427051604

        self.conn = conn
        self.vessel = self.conn.space_center.active_vessel
        self.realism_overhaul = realism_overhaul
        self.add_streams()
        self.do_descent()
        print("DONE!")

    def add_streams(self):

        self.planet = self.vessel.orbit.body
        self.ut = self.conn.add_stream(getattr, self.conn.space_center, 'ut')

        # Distance to surface
        # Todo: FIX( currently getting distance from center of mass which is problematic )
        self.surface_altitude = self.conn.add_stream(
            getattr, self.vessel.flight(), 'surface_altitude')

        # Vector of Retrograde
        # Todo: Check if the referenceFrame is correct
        self.retrograde = self.conn.add_stream(
            getattr, self.vessel.flight(), 'retrograde')

        self.prograde = self.conn.add_stream(
            getattr, self.vessel.flight(self.vessel.surface_reference_frame), 'prograde')

        self.elevation = self.conn.add_stream(
            getattr, self.vessel.flight(), 'elevation'
        )

        # Vertical Speed
        self.vertical_speed = self.conn.add_stream(
            getattr, self.vessel.flight(
                self.vessel.orbit.body.reference_frame), 'vertical_speed'
        )

        # Gravity
        self.g = self.conn.add_stream(getattr, self.planet, 'surface_gravity')

        # Total Mass
        self.mass = self.conn.add_stream(getattr, self.vessel, 'mass')
        # Total thrust
        self.maxthrust = self.conn.add_stream(
            getattr, self.vessel, 'max_thrust')
        print(self.maxthrust())

    def true_radar(self):
        return self.surface_altitude()-self.vessel_height

    def compute(self):
        max_decel = ((self.maxthrust() / 1000.0) /
                     (self.mass() / 1000)) - self.g()
        self.stop_dist = (
            math.pow(self.vertical_speed(), 2) / (2 * max_decel))
        self.ideal_throttle = max(
            min(1, self.stop_dist / self.true_radar()), self.engine_limit)
        self.impact_time = self.true_radar() / abs(self.vertical_speed())

    def do_descent(self):

        # Lock steering to retrograde on decent
        # Todo: Make steering head towards landing pad or vab
        # steering = steering_calculator()
        # steering.lock_auto_pilot(self.vessel, self.retrograde)
        self.extra_time = 0
        # self.extra_time += self.steering_controller.extra_time()

        # Initialize Variables and Streams
        self.throttle_control = False

        # Loop that calculates landing burn time and throttle
        # Todo: currently using two separate calculations for landing ideal throttle. add error for realism overhaul correction

        while True:
            # Update landing time calculations
            # Todo: create a UI panel inside ksp to display this info
            if self.vertical_speed() < 0:

                # print(self.conn)
                # self.conn.space_center.draw_direction(
                #     self.north, self.vessel.surface_reference_frame, (1, 0, 0))
                # self.conn.space_center.draw_direction(
                #     self.east, self.vessel.surface_reference_frame, (0, 1, 0))
                # self.conn.space_center.draw_direction(
                #     self.plane_normal, self.vessel.surface_reference_frame, (1, 1, 1))
                # self.conn.space_center.draw_direction(
                #     self.prograde, self.vessel.surface_reference_frame, (0, 0, 1))

                # Secondary ideal throttle calculations
                #!fix
                self.compute()
                print(self.ideal_throttle)
                if self.ideal_throttle >= 0.7:
                    self.throttle_control = True
                # ? Lock throttle to ideal throttle. this is because of loop
                if self.throttle_control:
                    self.vessel.control.throttle = self.ideal_throttle
                    if self.doing_flip:
                        self.steering_controller.flip(self.retrograde)

            # Todo: detect when landed using other methods
            # Detects when landing burn complete and vessel vertical speed is zeroed out.
            # doesn't account for horizontal
            #!fix
            if self.vertical_speed() >= 0:
                self.throttle_control = False
                self.vessel.control.throttle = 0
                break
            time.sleep(0.1)
