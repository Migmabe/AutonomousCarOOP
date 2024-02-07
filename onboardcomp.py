class BoardComputer:

    def __init__(self, status="off"):
        self.battery = Battery()
        self.status = status
        self.speed = 0
        self.rate = 0.01
        self.brake = False
        self.__manufacturer = "Mike Studios"
        self.__serialno = 1234567
        self.__software = "Studio 1.0"

    def __add__(self, choice):
        """adds and sets if the system is ON or OFF"""
        if choice is "off":
            self.status = "off"
        elif choice is "on":
            self.status = "on"
        else:
            raise ValueError("System can only be ON or OFF")

    def run_mode(self, input_data):
        while True:
            self.status = input("Do you want to start the system?: Please enter ON, OFF or (Q)uit").lower()
            for n in input_data:
                if self.status.lower() is "off":
                    print("System OFF")
                    break
                elif self.status.lower() is "on":
                    print("System ON")
                    console = ProcessUnit(IMU(), GNSS(), LightSensor(), NetworkAntenna(), ObstacleDetection())
                    chassis = HardwareControl()
                    console.run_mode(n)
                elif self.status.lower() is "Q":
                    break
                else:
                    print("Please enter a valid status.")
