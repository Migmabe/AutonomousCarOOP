from onboardcomp import BoardComputer
from processing import ProcessUnit

from csv import reader

#######################################################
date_time = 19  # 19 represents 19:00 hours or 7PM
light_threshold = 4

"""Here's the data that would supposedly come from sensors in real time"""
input_data = []
with open("files/x_y.csv") as g:
    csv_read = reader(g, delimiter=",")
    next(g)  # skip first titles row
    for t, a, orientation, latitude, longitude in csv_read:
        input_data.append([t, a, orientation, latitude, longitude])

#######################################################

if __name__ == "__main__":
    car1 = BoardComputer()
