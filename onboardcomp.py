class BoardComputer:

    def __init__(self, status="off"):
        self.battery = Battery()
        self.status = status
        self.speed = 0
        self.move = False
        self.__manufacturer = "Mike Studios"
        self.__serialno = 1234567
        self.__software = "Studio 1.0"
        self.process_data = {
            "Speed": 0,
            "Mileage": None,
            "Location": None
        }

    def __add__(self, computer_object):
        """Computer object can either be HardwareControl or ProcessUnit"""
        if type(computer_object).__name__ == "ProcessUnit":
            self.process_data["Location"] = computer_object.location

    def accelerate(self, value=5):
        self.move = True
        self.speed += value

    def brake(self, force_input=-5):
        if self.speed <= 0:
            print("Vehicle halted.")
        else:
            self.accelerate(force_input)

    def change_process_data(self, process_unit, hardware_control):
        self.process_data["Speed"] = (process_unit.speed + hardware_control.speed)/2  #average speed coming from sensors and mechanical
        self + process_unit



    def run_mode(self):
        while True:
            if self.status.lower() is "off":
                print("System OFF")
                break
            elif self.status.lower() is "on":
                print("System ON")
                while True:
                    console = ProcessUnit()
                    if self.move is True:
                        print(f"Moving... position coordinates {console.location}")
                    elif self.move is False:
                        print(f"Vehicle stopped at {console.location}")
