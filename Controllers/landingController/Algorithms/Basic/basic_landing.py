from ...LandingVessels.options import LoadOptions, SelectionMenu
import numpy as np
import math
import time


class suicide_burn_controller:
    def __init__(self, realism_overhaul, conn):
        self.conn = conn
        self.vessel = self.conn.space_center.active_vessel
        self.realism_overhaul = realism_overhaul
        self.set_profile()
        self.add_streams()
        self.steering_controller = steering_calculator(self.vessel)
        if self.doing_flip:
            self.steering_controller.starship_profile(self.prograde)
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

    def set_profile(self):
        loaded_profiles = LoadOptions().options
        display_name = []
        for key, value in loaded_profiles.items():
            # print(value["display_name"])
            display_name.append(value["display_name"])
        profile = SelectionMenu(display_name)
        selected_profile = loaded_profiles[profile.selected]
        print(selected_profile)

        # Set variables defaults
        self.spin_up_time = 0
        self.vessel_height = 0
        self.engine_mode = 1
        self.engine_mode_1 = 0
        self.engine_mode_2 = 0
        self.engine_mode_3 = 0
        self.doing_flip = False

        # Set variable values
        if len(selected_profile) > 0:
            try:
                try:
                    if selected_profile["doing_flip"]:
                        self.doing_flip = True
                except KeyError:
                    pass

                if self.realism_overhaul:
                    self.spin_up_time = selected_profile["spin_up_t"]
                else:
                    self.spin_up_time = 0
                self.vessel_height = selected_profile["dist_above_ground"]
                self.engine_modes = selected_profile["engine_modes"]
                if self.engine_modes > 1:
                    self.engine_mode_1 = selected_profile["max_thrusts"]["1"]
                    self.engine_mode_2 = selected_profile["max_thrusts"]["2"]
                    self.engine_mode_3 = selected_profile["max_thrusts"]["3"]
            except KeyError:
                print(
                    "Uh oh somthing when wrong when selecting profile ¯\_( ͡° ͜ʖ ͡°)_/¯")
        # Add ui if wanted

    def compute(self):
        max_decel = ((self.maxthrust() / 1000.0) /
                     (self.mass() / 1000)) - self.g()
        self.stop_dist = (
            math.pow(self.vertical_speed(), 2) / (2 * max_decel))
        self.ideal_throttle = self.stop_dist / self.true_radar()
        self.impact_time = self.true_radar() / abs(self.vertical_speed())

    def do_descent(self):

        # Lock steering to retrograde on decent
        # Todo: Make steering head towards landing pad or vab
        # steering = steering_calculator()
        # steering.lock_auto_pilot(self.vessel, self.retrograde)
        self.extra_time = 0
        self.extra_time += self.steering_controller.extra_time()
        if self.engine_modes > 1:
            handle_abnormal_engine = HandleAbnormalEngine(
                self.engine_mode_1, self.engine_mode_2, self.engine_mode_3,  self.vessel.control)
            handle_abnormal_engine.change_engine_mode(2)
            self.maxthrust = handle_abnormal_engine.current_available_thrust

        # Initialize Variables and Streams
        self.throttle_control = False
        computer = suicide_burn_calculator(
            self.conn, self.vessel, self.elevation())
        computer.add_stream(self.g, self.ut, self.mass, self.maxthrust)

        # Loop that calculates landing burn time and throttle
        # Todo: currently using two separate calculations for landing ideal throttle. add error for realism overhaul correction

        while True:
            # Update landing time calculations
            time_until_burn = computer.update()
            # Todo: create a UI panel inside ksp to display this info
            print(time_until_burn)
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
                if time_until_burn - self.spin_up_time < 0:
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


class HandleAbnormalEngine:
    def __init__(self, thrust_1, thrust_2, thrust_3, control):
        self.thrust_1 = thrust_1
        self.thrust_2 = thrust_2
        self.thrust_3 = thrust_3
        self.control = control

    def change_engine_mode(self, mode):
        if mode == 1:
            # ? All Engines
            self.current_thrust = self.thrust_1
            self.control.set_action_group(1, False)
            self.control.set_action_group(2, False)
            print("Current Thrust Changed to: ", self.current_thrust)
        elif mode == 2:
            # ? Three Engines
            self.current_thrust = self.thrust_2
            self.control.set_action_group(1, True)
            self.control.set_action_group(2, False)
            print("Current Thrust Changed to: ", self.current_thrust)
        elif mode == 3:
            # ? One Engine
            self.current_thrust = self.thrust_3
            self.control.set_action_group(1, True)
            self.control.set_action_group(2, True)
            print("Current Thrust Changed to: ", self.current_thrust)

    def current_available_thrust(self):
        return self.current_thrust


###############################################################################
# Burn Calculator Class
###############################################################################


class suicide_burn_calculator(object):
    '''
    Class that calculates time until suicide burn.
    '''

    def __init__(self, conn, v, alt):
        self.conn = conn
        self.v = v
        self.sc = conn.space_center
        self.burn_time = np.inf
        self.burn_duration = np.inf
        self.ground_track = np.inf
        self.effective_decel = np.inf
        self.radius = np.inf
        self.angle_from_horizontal = np.inf
        self.impact_time = np.inf
        self.alt = alt
        self.planet = self.v.orbit.body

        self.rf = self.sc.ReferenceFrame.create_hybrid(
            position=self.v.orbit.body.reference_frame,
            rotation=self.v.surface_reference_frame)

    def add_stream(self, g, ut, mass, max_thrust):
        self.velocity = self.conn.add_stream(
            getattr, self.v.flight(
                self.rf), 'velocity'
        )

        self.periapsis = self.conn.add_stream(
            getattr, self.v.orbit, 'periapsis_altitude'
        )

        # Gravity
        # self.g = self.conn.add_stream(getattr, self.planet, 'surface_gravity')
        self.g = g

        self.speed = self.conn.add_stream(
            getattr, self.v.flight(
                self.rf), 'speed'
        )

        # self.ut = self.conn.add_stream(getattr, self.conn.space_center, 'ut')
        self.ut = ut

        # self.mass = self.conn.add_stream(getattr, self.v, 'mass')
        self.mass = mass

        # self.max_thrust = self.conn.add_stream(
        #     getattr, self.v, 'max_thrust')
        self.max_thrust = max_thrust
        self.equatorial_radius = self.conn.add_stream(
            getattr, self.planet, 'equatorial_radius')

    def update(self):
        '''
        Returns an estimate of how many seconds until you need to burn at 95% throttle to avoid crashing.
        This gives a 5% safety margin.
        I do not even PRETEND to understand all of the math in this function.  It's essentially a porting
        of the routine from the Mechjeb orbit extensions.
        '''

        # We're not on a landing trajectory yet.
        if self.periapsis() > 0:
            self.burn_time = np.inf
            self.burn_duration = np.inf
            self.ground_track = np.inf
            self.effective_decel = np.inf
            self.angle_from_horizontal = np.inf
            self.impact_time = np.inf
            return self.burn_time

        # self.rf =

        # calculate sin of angle from horizontal -
        v1 = self.velocity()
        v2 = (0, 0, 1)
        self.angle_from_horizontal = angle_between(v1, v2)
        sine = math.sin(self.angle_from_horizontal)

        # estimate deceleration time
        # calculating with 5% safety margin!
        T = (self.max_thrust() / self.mass()) * .95
        self.effective_decel = .5 * \
            (-2 * self.g() * sine + math.sqrt((2 * self.g() * sine)
                                              * (2 * self.g() * sine) + 4 * (T*T - self.g()*self.g())))
        self.decel_time = self.speed() / self.effective_decel

        # estimate time until burn
        radius = self.equatorial_radius() + self.alt
        TA = self.v.orbit.true_anomaly_at_radius(radius)
        TA = -1 * TA  # look on the negative (descending) side of the orbit
        self.impact_time = self.v.orbit.ut_at_true_anomaly(TA)
        # self. impact_place = self.v.orbit.position_at(
        #     self.impact_time, self.v.orbit.body.reference_frame)
        # # print(self.impact_place)
        self.burn_time = self.impact_time - self.decel_time/2
        self.ground_track = ((self.burn_time - self.ut()) * self.speed()) + (
            .5 * self.speed() * self.decel_time)
        return self.burn_time - self.ut()

###############################################################################
# Steering Calculator Class
###############################################################################


class steering_calculator(object):
    def __init__(self, vessel):
        self.vessel = vessel
        # self.ap.reference_frame = self.vessel.orbit.body.reference_frame
        # self.control = vessel.control
        # self.ap = vessel.auto_pilot
        # print("AUTO PILOT ENGAGED")

        # self.ap.reference_frame = self.vessel.surface_reference_frame
        # self.ap.engage()
        # self.ap.target_direction = (0, 0, 0)
        # self.control.rcs = True

    # def lock_auto_pilot(self, vessel, retrograde):
    #     self.ap = vessel.auto_pilot
    #     self.control.sas = True
    #     # self.ap.engage()
    #     self.app.reference_frame = vessel.surface_reference_frame
    #     # ap.wait()

    def extra_time(self):
        return 3

    def starship_profile(self, prograde):
        # self.ap.target_direction = (0, 0, 1)
        # self.ap.target_direction = prograde()
        # self.ap.target_heading = 90
        # self.ap.reference_frame = self.vessel.orbit.body.reference_frame
        # self.ap.target_pitch = prograde()[]
        # self.ap.target_pitch = 0
        # print(prograde()[1])
        # self.ap.target_heading = 0

        # print("Vessel direction", self.vessel.direction(
        #     self.vessel.surface_reference_frame)[1])
        # self.ap.target_roll = 0
        # self.ap.target_heading = 270
        pass

    def flip(self, retrograde):

        try:
            self.control.set_action_group(6, False)
            self.control.set_action_group(5, False)
        except:
            pass


###############################################################################
# Vector Math Functions        -   Probably ought to move to their
# own library file some day.
###############################################################################

def unit_vector(vector):
    """ Returns the unit vector of the vector provided.  """
    return vector / np.linalg.norm(vector)


def angle_between(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'"""
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))
