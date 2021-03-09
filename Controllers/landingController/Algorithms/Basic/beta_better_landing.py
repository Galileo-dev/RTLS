

import time


class lander_doer(object):
    def __init__(self, conn):
        self.conn = conn
        self.vessel = self.conn.space_center.active_vessel
        self.throttle_control = False
        self.add_streams()
        self.do_landing()

    def do_landing(self):
        while self.vessel.situation != self.conn.space_center.VesselSituation.landed:
            TWR = max(0.001, self.maxthrust() / (self.mass() * self.g()))
            ideal_throttle = (0.85 / TWR) - min(0, (self.vertical_speed() +
                                                    max(5, min(350, self.surface_altitude() ** 1.06 / 5))) / 3 / TWR)
            if ideal_throttle > 0.95:
                self.throttle_control = True

            if self.throttle_control:
                self.vessel.control.throttle = ideal_throttle
            print(ideal_throttle)
            time.sleep(0.01)

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
