
import keyboard


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
                "name": "sn9",                   # name of vessel
                "display_name": "Serial #9",  # distance of root module above ground
                "dist_above_ground": 11.383058855892159,
                "spin_up_t": 4.387001037597656,   # in ms
                "engine_modes": 1,
                "doing_flip": True
            },
            5: {
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
            6: {
                "name": "unknown",                   # name of vessel
                "display_name": "Unknown",
                # distance of root module above ground
                "dist_above_ground": 0,
                "engine_modes": 1,
                "spin_up_t": 0,
            }
        }


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
