# Here all the modules connected to the Process Unit class
from onboardcomp import BoardComputer
from csv import reader

#######################################################
"""Here's the data that would supposedly come from sensors in real time"""
coord = []
with open("files/x_y.csv") as coordinates:
    csv_read = reader(coordinates, delimiter=",")
    next(coordinates)  # skip first titles row
    for x, y in csv_read:
        coord.append([x, y])


#######################################################

class ProcessUnit(BoardComputer):

    def __init__(self, imu_object):
        super().__init__()
        self.error_list = []
        self.error_count = 0
        self.imu = imu_object

    def __setattr__(self, key, value):
        print(f"Setting {key} to {value}")
        super().__setattr__(key, value)

    @property
    def location(self):
        """do average between get_position and get_location"""
        if self.imu.position is not None and


class NetworkAntenna:
    pass


class GNSS:

    def __init__(self, latitude=0, longitude=0):


class ObstacleDetection:
    pass


class IMU:
    """With acceleration over time and orientation, it can get its position in coordinates"""

    def __init__(self, acceleration=0):
        self.acceleration = acceleration
        self._orientation = None
        self._position = None

    @property
    def orientation(self):
        return self._orientation

    @orientation.setter
    def orientation(self, new_value):
        if type(new_value) is not int or float:
            self._orientation.cardinal_directions(new_value)
        else:
            self._orientation = new_value

    def cardinal_directions(self, direction):
        if direction.lower() == "north":
            self._orientation = 90
        elif direction.lower() == "south":
            self._orientation = 270
        elif direction.lower() == "east":
            self._orientation = 0
        elif direction.lower() == "west":
            self._orientation = 180

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, new_value):
        self._position = new_value


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
