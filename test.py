from csv import reader

input_data = []

with open("files/x_y.csv") as g:
    csv_read = reader(g, delimiter=",")
    next(csv_read)  # skip the first row (titles)

    for row in csv_read:
        # Ensure the row has exactly 5 values
        if len(row) == 5:
            t, a, orientation, latitude, longitude = row

            # Convert latitude and longitude to float (example conversion)
            latitude = float(latitude)
            longitude = float(longitude)

            input_data.append([t, a, orientation, latitude, longitude])
        else:
            print(f"Skipping row {row} as it does not have 5 values.")

# Print the resulting data
for data in input_data:
    print(data)
