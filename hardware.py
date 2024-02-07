class HardwareControl:

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