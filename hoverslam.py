import math
from math import trunc
from sys import setrecursionlimit
import time
import krpc
import keyboard
from libs import SelectionMenu, steering_calculator, suicide_burn_calculator, LoadOptions,  HandleAbnormalEngine
# from libs import SelectionMenu

###############################################################################
# Constants
# Option for ui to be enabled inside ksp
ui = False
#
# Allow re-entry burn based on calculations otherwise your
# vessel may heat up too much and explode!💥
allow_reentry = True
#
# If realsim overhaul is installed set this to True. it will take into account
# Engine startup time this can be found via "get_options.py" which can then be put
# in options.py
realism_overhaul = False
#
#
###############################################################################


class Hoverslam:

    # Set up streams for telemetry

    def __init__(self):
        self.conn = krpc.connect()
        self.vessel = self.conn.space_center.active_vessel
        self.set_profile()
        self.add_streams()
        self.steering_controller = steering_calculator(self.vessel)
        if self.doing_flip:
            self.steering_controller.starship_profile(self.prograde)
        self.do_descent()

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

    # Pre-landing setup

    def pre_landing_setup(self):
        # self.vessel.control.sas = False
        self.vessel.control.rcs = False
        self.vessel.control.throttle = 1.0

    # def load_profile(self):
    #     options = ['f9', 'starship', 'falcon-heavy']
    #     menu = SelectionMenu(options).selected
    #     print(menu)

    def count_down_to_land(self):
        # Countdown...
        # todo: make this accurate
        print('3...')
        time.sleep(1)
        print('2...')
        time.sleep(1)
        print('1...')
        time.sleep(1)
        print('Landed!')

    # Activate the first stage
    def stage(self):
        self.vessel.control.activate_next_stage()

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

                if realism_overhaul:
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

    def true_radar(self):
        return self.surface_altitude()-self.vessel_height

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

            # if self.maxthrust() == 0:
            #     self.maxthrust = handle_abnormal_engine.current_available_thrust
            # print(self.maxthrust())
            # Update landing time calculations
            time_until_burn = computer.update()
            # Todo: create a UI panel inside ksp to display this info
            print(time_until_burn)
            if self.vertical_speed() < 0:
                # Secondary ideal throttle calculations
                #!fix
                self.compute()
                if time_until_burn - self.spin_up_time - self.extra_time < 0:
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
            if self.vertical_speed() >= 0.01:
                self.sas = False
                self.throttle_control = False
                self.vessel.control.throttle = 0

                break
            time.sleep(0.1)


doHoverslam = Hoverslam()
