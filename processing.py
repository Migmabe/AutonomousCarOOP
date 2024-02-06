# Here all the modules connected to the Process Unit class

class ProcessUnit:

    def __init__(self):
        self.error_list = []
        self.error_count = 0

    """def running(self):
        while True:
            if"""





class NetworkAntenna:
    pass


class GNS:
    pass


class ObstacleDetection:
    pass


class IMU(ProcessUnit):
    """With acceleration over time and orientation, it can get its position in coordinates"""

    orientations = {
        "north": 90,
        "west": 180,
        "south": 270,
        "east": 0
    }

    def __init__(self, acceleration):
        super().__init__()
        self.acceleration = acceleration
        self._orientation = None

    @property
    def orientation(self):
        return self._orientation

    @orientation.setter
    def orientation(self, new_value):
        if type(new_value) is str:
            self.error_log("Orientation must be a cardinal direction or a number")

    def translate(self, value):
        self.orientation = self.orientations[value]
        return self.orientation

        print("Orientation...")
        if new_value.lower() in ["north", "south", "east", "west"]:
            self.translate(new_value.lower())
        elif new_value.isnumeric():
            self.orientation = new_value
        else:
            raise ValueError("Invalid input")


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
