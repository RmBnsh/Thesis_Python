import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.style.use('seaborn')
# Read the CSV file
narg = len(sys.argv)
if narg >= 2:
    filename = sys.argv[1]
else:
    filename = input('Enter filename to plot: ')

dataframe = pd.read_csv(filename)

# Extract the required columns
time = pd.to_datetime(dataframe['time'], format='%Y-%m-%dT%H:%M:%SZ')
elevation = dataframe['ele']
speed = dataframe['speed']

speed = speed * 3.6
dt = time - np.roll(time, 1)
dt[0] = dt[1]
# Plotting the data
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7.5, 10))


# Plot 1: Elevation
ax1.plot(time, elevation, color='orange')
ax1.set_xlabel('Time')
ax1.set_ylabel('Elevation')
ax1.set_title('Elevation')
ax1.set_xlim(min(time), max(time))
# Plot 2: Speed
ax2.plot(time, speed, color='orange')
ax2.set_xlabel('Time')
ax2.set_ylabel('Speed')
ax2.set_title('Speed')
ax2.set_xlim(min(time), max(time))

print("Average speed [km/h]", np.average(speed))
print("Max speed [km/h]", np.max(speed))
print("Distance [m]", np.sum(speed * dt))

plt.tight_layout()
plt.show()
