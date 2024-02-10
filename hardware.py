from onboardcomp import *


class HardwareControl(ProcessUnit):

    def __init__(self):
        super().__init__(imu_object=None, gnss_object=None, light_sensor_object=None, obstacle_detection_object=None)
        self.hardware = ElectricalMotor(self.speed, self.status).error()

    def error(self):
        self.error_list.append(self.hardware)
        self.error_count = len(self.error_list)

    """Here we use the updater function inherited from the class to retrofeed the data to the computer"""


class Light:

    def __init__(self, brightness, blink_rate, colour):
        self.brightness = brightness
        self.blink_rate = blink_rate
        self.colour = colour

    def error(self, hardware):
        if type(self.colour) is not str:
            hardware.errors.append("Colour must be a string")
        if type(self.brightness) is str:
            hardware.errors.append("Brightness must be a number")
        if type(self.colour) is str:
            hardware.errors.append("Blink rate must be a number")


class ElectricalMotor:

    def __init__(self, linear_vel, status):
        self.linear_vel = linear_vel
        self.wheel = Wheel(status).error()
        self.angular_velocity = 2 * self.linear_vel / self.wheel.size  # 2 added as the wheel size is the diameter not radius

    def error(self):
        if self.linear_vel < 0:
            self.wheel.append("Linear velocity reverted in electrical motor level")
        return self.wheel


class Wheel:

    def __init__(self, status):
        self.size = 17
        self.brake = Brake(status).error(status)  # returns a list of errors and creates light objects

    def error(self):
        if self.size > 18:
            self.brake.append("Wheel size bigger than 18")
        if type(self.size) is str:
            self.brake.append("Wheel size invalid")
        return self.brake


class Brake:

    def __init__(self, status):
        self.errors = []
        if status is True:
            self.light_on()
        else:
            self.light_off()

    def light_on(self):
        return Light(100, 0, "red").error(self)

    def light_off(self):
        return Light(0, 0, "red").error(self)

    def error(self, status):
        if type(status) is not bool:
            self.errors.append("Braking status invalid")
            return self.errors
