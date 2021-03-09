
# from Controllers.landingController.Algorithms.Basic.beta_better_landing import lander_doer
from Controllers.landingController.Algorithms.Basic.basic_landing import suicide_burn_controller
import krpc
import time
import math
from launch import Launch


class Rocket:

    def __init__(self):
        self.connect_krpc()

    def connect_krpc(self):
        self.conn = krpc.connect()
        self.vessel = self.conn.space_center.active_vessel

    def launch(self, target_apoapis, turn_start, turn_end):
        launch_controller = Launch(target_apoapis, turn_start, turn_end)

    def land(self, ):
        # algorithm, landing_pad

        self.landing_controller = suicide_burn_controller(
            realism_overhaul=False, conn=self.conn)


    # def boost_back(self, algorithm, landing_pad):
    #     pass
rocket_controller = Rocket()

turn_start_altitude = 250
turn_end_altitude = 45000
target_altitude = 150000

# rocket_controller.launch(
#     target_altitude, turn_start_altitude, turn_end_altitude)
rocket_controller.land()
