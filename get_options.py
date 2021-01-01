import krpc
import time


class get_options:
    def __init__(self):
        self.conn = krpc.connect()
        self.vessel = self.conn.space_center.active_vessel
        self.get_height()
        # self.get_spin_up_time()

    def get_height(self):

        # Add streams
        self.surface_altitude = self.conn.add_stream(
            getattr, self.vessel.flight(), 'surface_altitude')

        if self.vessel.situation == self.conn.space_center.VesselSituation.landed:
            print("Height above ground is", self.surface_altitude())
        else:
            print("You must be on level ground and stationary for accurate readings")

    # Print()

    def get_spin_up_time(self):
        # Add streams
        # maxthrust = self.conn.add_stream(
        #     getattr, self.vessel, 'max_thrust')
        thrust = self.conn.add_stream(
            getattr, self.vessel, 'thrust')
        available_thrust = self.conn.add_stream(
            getattr, self.vessel, 'available_thrust')

        print(thrust(), available_thrust())
        self.vessel.control.throttle = 1.0
        start = time.time()
        while thrust() <= available_thrust():
            time.sleep(0.01)
            print(thrust())
        end = time.time()
        self.vessel.control.throttle = 0
        print("Spin up time is", end - start)
        #!todo: add a code to slowly lower vessel to stop it smashing into ground


get_options()
