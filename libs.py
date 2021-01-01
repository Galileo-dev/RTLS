import keyboard
import krpc
import math
import time
from krpc.schema.KRPC_pb2 import Error
import numpy as np


###############################################################################
# Load profiles
###############################################################################

class LoadOptions:
    def __init__(self):
        self.options = {
            1: {
                "name": "new_shepard",                   # name of vessel
                "display_name": "New Shepard",
                "dist_above_ground": 5.097551461542025,  # distance of root module above ground
                "spin_up_t": 4,
                "engine_modes": 1,                      # in ms
            },
            2: {
                "name": "f9",                   # name of vessel
                "display_name": "Falcon 9",
                "dist_above_ground": 5.097551461542025,  # distance of root module above ground
                "engine_modes": 3,
                "spin_up_t": 5.1519997119903564,
                "max_thrusts": {
                    "1": 7638074.0,
                    "2": 2546000.0,
                    "3": 848800
                },
            },
            3: {
                "name": "starship",                   # name of vessel
                "display_name": "Starship",  # distance of root module above ground
                "dist_above_ground":   10.542455316404812,
                "spin_up_t": 4.387001037597656,   # in ms
                "engine_modes": 1,
                "doing_flip": True
            },
            4: {
                "name": "sh",                   # name of vessel
                "display_name": "Super Heavy",
                # distance of root module above ground
                "dist_above_ground": 17.999085182556883,
                "engine_modes": 2,
                "spin_up_t": 5.1519997119903564,
                "max_thrusts": {
                    "1": 7638074.0,
                    "2": 2546000.0
                },
            },
            5: {
                "name": "unknown",                   # name of vessel
                "display_name": "Unknown",
                # distance of root module above ground
                "dist_above_ground": 0,
                "engine_modes": 1,
                "spin_up_t": 0,
            }
        }


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


class SelectionMenu:
    def __init__(self, options):
        print("Please select a profile")
        self.selected = 1
        self.options = options
        self.show_menu()
        keyboard.add_hotkey('up', self.up)
        keyboard.add_hotkey('down', self.down)
        keyboard.wait('enter')

    def show_menu(self):
        self.selected
        print("\n" * 30)
        print("Choose an option:")
        for i in range(1, len(self.options) + 1):
            print("{1} {0}. {3} {2}".format(
                i, ">" if self.selected == i else " ", "<" if self.selected == i else " ", self.options[i - 1]))

    def up(self):
        self.selected
        if self.selected == 1:
            return
        self.selected -= 1
        self.show_menu()

    def down(self):
        self.selected
        if self.selected == 4:
            return
        self.selected += 1
        self.show_menu()


# options = ['f9', 'starship', 'falcon-heavy']
options = LoadOptions().options  # .options[1]["display_name"]


# print(display_name)
# print(options)
# menu = SelectionMenu(options).selected
# print(menu)


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


###############################################################################
# Steering Calculator Class
###############################################################################

class steering_calculator(object):
    def __init__(self, vessel):
        self.ap = vessel.auto_pilot
        self.vessel = vessel
        # self.ap.reference_frame = self.vessel.orbit.body.reference_frame
        self.control = vessel.control
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
        # self.ap.target_direction = prograde()
        # self.ap.target_heading = 90
        self.ap.reference_frame = self.vessel.surface_reference_frame
        # self.ap.reference_frame = self.vessel.orbit.body.reference_frame
        # self.ap.target_pitch = prograde()[]
        print(prograde())
        self.ap.target_direction = prograde()
        self.ap.target_roll = 0
        # self.ap.target_heading = 270
        self.ap.engage()

    def flip(self, retrograde):
        self.ap.disengage()
        self.control.sas = True
        self.control.rcs = True
        try:
            self.control.sas_mode = self.control.sas_mode.retrograde
            # self.ap.target_direction = retrograde()
            self.control.set_action_group(6, False)
            self.control.set_action_group(5, False)
        except:
            pass

###############################################################################
# UI Class
###############################################################################


class ui(object):
    def __init__(self, conn):
        self.conn = conn
        self.canvas = self.conn.ui.stock_canvas
        # Get the size of the game window in pixels
        screen_size = self.canvas.rect_transform.size
        self.panel = self.canvas.add_panel()

        self.rect = self.panel.rect_transform
        self.rect.size = (200, 100)
        self.rect.position = (110-(screen_size[0]/2), 0)

        # Add a button to set do hoverslam to true
        self.button = self.panel.add_button("Do hoverslam")
        self.button.rect_transform.position = (0, 20)

        self.button_clicked = conn.add_stream(getattr, self.button, 'clicked')
