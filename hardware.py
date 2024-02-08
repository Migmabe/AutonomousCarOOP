from processing import ProcessUnit


class HardwareControl(ProcessUnit):

    def __init__(self, chassis_object):
        self.health_issues = 0
        self.health_log = []
        self.chassis = chassis_object
        self.process_data = {
            "Speed": 0,
            "Mileage": 0
        }


class Chassis:
    pass


class Light:

    def __init__(self, brightness, blink_rate, colour):
        self.brightness = brightness
        self.blink_rate = blink_rate
        self.colour = colour

    def set_colour(self, new_colour):
        self.colour = new_colour


class ElectricalMotor:

    def __init__(self):
        self.odometer_reading = 0
        self.wheel = Wheel()


    def linear_velocity(self):



class Wheel:

    def __init__(self):
        self.size = 17



