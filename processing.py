# Here all the modules connected to the Process Unit class
from onboardcomp import BoardComputer


class ProcessUnit(BoardComputer):

    def __init__(self, imu_object, gnss_object, light_sensor_object, network_antenna_object, obstacle_detection_object):
        super().__init__()
        self.error_list = []
        self.error_count = 0
        self.imu = imu_object
        self.gnss = gnss_object
        self.lightsensor = light_sensor_object
        self.networkantenna = network_antenna_object
        self.obstacle_detection = obstacle_detection_object
        self.process_data = {
            "Speed": 0,
            "Location": None,
            "Lights": bool(0)
        }

    def accelerate(self):
        """where acceleration comes from IMU and times from CSV - mainly used in"""
        if self.brake is False:
            self.speed += self.imu.acceleration * self.rate
            self.process_data["Speed"] = self.speed
            print(f"Speed is now: {self.speed}")
        elif self.brake is True:
            self.speed -= self.imu.acceleration * self.rate
            self.process_data["Speed"] = self.speed
            print(f"Speed is now: {self.speed}")

    def brake(self):
        while self.speed > 0:
            self.accelerate()
        if self.speed <= 0:
            print("Vehicle halted.")

    def run_mode(self, n):
        while True:

                if self.brake is False:
                    print(f"Moving... position coordinates {self.location}")
                    self.accelerate()  #assummed time interval of 0.01 --> feedback rate from sensors 100Hz
                elif self.brake is True:
                    self.brake()
                    print(f"Vehicle stopped at {self.location}")
                    break


    def __setattr__(self, key, value):
        print(f"Setting {key} to {value}")
        super().__setattr__(key, value)


    def location(self):
        """do average between get_position and get_location"""
        if self.imu.position is not None and self.gnss.get_location() is not None:
            return


    def lights(self):
        if self.lightsensor.threshold > 3:
            self.process_data["Lights"] = bool(0)
        else:
            self.process_data["Lights"] = bool(1)



class NetworkAntenna:
    pass


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

    def __init__(self, range_ = 50):
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

    def __init__(self, acceleration=0):
        self.acceleration = acceleration
        self._orientation = None
        self._position = [0, 0]

    @property
    def orientation(self):
        return self._orientation

    @orientation.setter
    def orientation(self, new_value):
        if type(new_value) is not int or float:
            self._orientation.cardinal_directions(new_value)
        else:
            self._orientation = new_value


    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, new_value):
        self._position = new_value


    def cardinal_directions(self, direction):
        if direction.lower() == "north":
            self._orientation = 90
        elif direction.lower() == "south":
            self._orientation = 270
        elif direction.lower() == "east":
            self._orientation = 0
        elif direction.lower() == "west":
            self._orientation = 180
        else:
            raise ValueError("Invalid orientation")

    def get_acceleration(self, new_value):
        """where new_value must be the 2nd column of the row being called in input_data[2]"""
        self.acceleration = new_value



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
