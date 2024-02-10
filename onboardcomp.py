import math


class BoardComputer:

    def __init__(self, destination=(0, 100), status="off", network_antenna_object=None):
        if network_antenna_object is None:
            self.networkantenna = NetworkAntenna()
        self.mileage = Battery().mileage()
        self.status = status
        self.speed = 0
        self.rate = 0.01
        self.brake = True
        self.__manufacturer = "Mike Studios"
        self.__serialno = 1234567
        self._software = 1.0
        self.destination = destination

    def __add__(self, choice):
        """adds and sets if the system is ON or OFF"""
        if choice == "off":
            self.status = "off"
        elif choice == "on":
            self.status = "on"
        else:
            raise ValueError("System can only be ON or OFF")

    @property
    def software(self):
        return self._software

    @software.setter
    def software(self, new):
        self._software = new

    def ov_check(self, latest_OV):
        if self.software < latest_OV:
            self.software = latest_OV
            print(f"Software updated to version {self.software}")

    def run_mode(self, input_data, latest_OV, light_threshold):
        while True:
            self + input("Do you want to start the system?: Please enter ON, OFF or (Q)uit").lower()
            if self.status.lower() == "off":
                print("System OFF")
                break
            elif self.status.lower() == "on":
                print("System ON")
                self.ov_check(latest_OV)
                console = ProcessUnit(IMU(), GNSS(), LightSensor(light_threshold), ObstacleDetection())
                for n in input_data:
                    if console.run_mode(n, self) == "Exit":
                        break
            elif self.status.lower() == "Q":
                break
            else:
                print("Please enter a valid status.")


class NetworkAntenna:
    rate = 0.01

    def __init__(self):
        self.status = "on"


class Battery:

    def __init__(self, discharge=10000):
        self.capacity = 30000
        self.discharge_rate = discharge  # per hour

    def mileage(self):
        """at an assumed average speed of 60 kmh || not in real time"""
        time = self.capacity / self.discharge_rate
        mileage = time * 60
        return mileage


######################################################################################

class ProcessUnit(BoardComputer):

    def __init__(self, imu_object, gnss_object, light_sensor_object, obstacle_detection_object):
        super().__init__()
        self.error_list = []
        self.error_count = 0
        self.imu = imu_object
        self.gnss = gnss_object
        self.lightsensor = light_sensor_object
        self.obstacle_detection = obstacle_detection_object
        self.process_data = {
            "Speed": 0,
            "Location": [0, 0],
            "Lights": bool(0)
        }

    def updater(self, upper_object):
        """where car1 is my car object or hardware control object"""
        if isinstance(upper_object, BoardComputer):
            upper_object.brake = self.brake
            upper_object.speed = self.speed
        elif isinstance(upper_object, HardwareControl):
            self.error_count = upper_object.error_count
            self.error_list = upper_object.error_list

    def accelerate(self, input_data):
        """where acceleration comes from IMU and times from CSV - mainly used in"""
        if self.brake is False:
            self.speed = self.speed + self.imu.get_acceleration(input_data) * self.rate
            self.process_data["Speed"] = self.speed
            print(f"Speed is now: {self.speed}")
        elif self.brake is True:
            self.speed = self.speed - self.imu.get_acceleration(input_data) * self.rate
            self.process_data["Speed"] = self.speed
            print(f"Speed is now: {self.speed}")

    def brake_func(self, location):
        """where input is location list[] from imu"""
        print(f"Vehicle braking. Position {location}")
        while self.speed > 0:
            self.accelerate()
        if self.speed <= 0:
            print(f"Vehicle halted at {location}")

    def choice(self, n):
        self.obstacle_detection.get_obstacle(n)
        if self.obstacle_detection.obstacle is True:
            self.brake = True
        elif self.obstacle_detection.obstacle is False:
            self.brake = False

    def run_mode(self, n, car1):
        self.lights()
        HardwareControl().updater(self)
        if self.process_data["Location"][1] >= self.destination[1]:
            print("You have arrived!")
            self.updater(car1)
            car1.status = "off"
            return "Exit"
        else:
            self.choice(n)
            if self.brake is False:
                self.accelerate(n)  # assumed time interval of 0.01 --> feedback rate from sensors 100Hz
                pos = self.location(n)
                print(f"Moving... position coordinates {pos}")
            elif self.brake is True:
                pos = self.location(n)
                self.brake_func(pos)

    def location(self, n):
        """do average between get_position and get_location"""
        if self.imu.position is not None and self.gnss.location is not None:
            self.process_data["Location"] = self.imu.new_position(n)
            return self.imu.new_position(n)

    def lights(self):
        if self.lightsensor.threshold > 3:
            self.process_data["Lights"] = bool(1)
            print("Lights ON")
        else:
            self.process_data["Lights"] = bool(0)
            print("Lights OFF")


class GNSS:

    def __init__(self, latitude=0, longitude=0):
        self._latitude = latitude
        self._longitude = longitude
        self.speed = 0

    @property
    def location(self):
        return [self._latitude, self._longitude]

    @location.setter
    def location(self, new_value):
        """where new_value is basically input data n[3] and n[4]"""
        self.location = [new_value[3], new_value[4]]


class ObstacleDetection:

    def __init__(self, range_=50):
        """where range is in metres"""
        self.__range = range_
        self.obstacle = False

    def get_obstacle(self, n):
        if n[5] is True:
            self.obstacle = True
        else:
            self.obstacle = False


class IMU:
    """With acceleration over time and orientation, it can get its position in coordinates"""

    rate = 0.01  # in this case corresponds to the one from the OnBoardComputer but it may not as it is an individual

    # component on its own

    def __init__(self, acceleration=0):
        self.acceleration = acceleration
        self._orientation = [0, 0]
        self._position = [0, 0]

    @property
    def orientation(self):
        return self._orientation

    @orientation.setter
    def orientation(self, new_value):
        """where the orientation must be the 3rd column value or input_data[2]"""
        if type(new_value[2]) is str:
            self.cardinal_directions(new_value[2])
        else:
            self._orientation = [math.sin(new_value[2]), math.cos(new_value[2])]

    @property
    def position(self):
        return self._position

    def cardinal_directions(self, direction):
        """where direction == new_value from orientation function"""
        if direction.lower() == "north":
            self._orientation = [0, 1]
        elif direction.lower() == "south":
            self._orientation = [0, -1]
        elif direction.lower() == "east":
            self._orientation = [1, 0]
        elif direction.lower() == "west":
            self._orientation = [-1, 0]
        else:
            raise ValueError("Invalid orientation")

    def get_acceleration(self, input_data):
        """where new_value must be the 2nd column of the row being called in input_data[1]"""
        self.acceleration = float(input_data[1])
        return self.acceleration

    def new_position(self, input_data):
        self.orientation = input_data
        [self.position[0], self.position[1]] = [
            math.cos(self.orientation[0]) * (self.position[0] + (self.rate ** 2) * self.get_acceleration(input_data)),
            math.sin(self.orientation[1]) * (self.position[1] + (self.rate ** 2) * self.get_acceleration(input_data))]
        return self.position


class LightSensor:
    """Sets the light sensor, absolute darkness being 0"""

    def __init__(self, threshold=0):
        self._threshold = threshold

    @property
    def threshold(self):
        return self._threshold

    @threshold.setter
    def threshold(self, new_value):
        if type(new_value) is int:
            self._threshold = new_value
        else:
            raise ValueError("Light Threshold must be numerical")


############################################################################################

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
        self.wheel = Wheel(status)
        self.errors = Wheel(status).error()
        self.angular_velocity = 2 * self.linear_vel / self.wheel.size  # 2 added as the wheel size is the diameter not radius

    def error(self):
        if self.linear_vel < 0:
            self.errors.append("Linear velocity reverted in electrical motor level")
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
