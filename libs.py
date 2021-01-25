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
