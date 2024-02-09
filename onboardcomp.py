class BoardComputer:

    def __init__(self, destination=(100, 0), status="off", network_antenna_object=None):
        if network_antenna_object == None:
            self.networkantenna = NetworkAntenna()
        self.battery = Battery()
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
        if choice is "off":
            self.status = "off"
        elif choice is "on":
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

    def run_mode(self, input_data):
        while True:
            self + input("Do you want to start the system?: Please enter ON, OFF or (Q)uit").lower()
            for n in input_data:
                if self.status.lower() is "off":
                    print("System OFF")
                    break
                elif self.status.lower() is "on":
                    print("System ON")
                    self.ov_check()
                    console = ProcessUnit(IMU(), GNSS(), LightSensor(), ObstacleDetection())
                    console.run_mode(n)
                elif self.status.lower() is "Q":
                    break
                else:
                    print("Please enter a valid status.")


class NetworkAntenna:
    rate = 0.01

    def __init__(self):
        self.status = "on"
