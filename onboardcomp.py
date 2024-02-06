class BoardComp:

    def __init__(self, status="off"):
        self.status = status
        self.speed = 0
        self.move = False
        self.__manufacturer = "Mike Studios"
        self.__serialno = 1234567
        self.__software = "Studio 1.0"
        self.process_data = {}

    def accelerate(self, value=5):
        self.move = True
        self.speed += value

    def brake(self, force_input=-5):
        if self.speed <= 0:
            print("Vehicle halted.")
        else:
            self.accelerate(force_input)

    def run_mode(self, process_unit, chassis):
        while True:
            if self.status is "off":
                print("System OFF")
                break
            elif self.status is "on":
                while True:
                    if self.move is True:
                        print(f"Moving... position coordinates {process_unit.location}")
                    elif self.move is False:
                        print(f"Vehicle stopped at {process_unit.location}")
