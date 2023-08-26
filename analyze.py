import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.style.use('classic')

narg = len(sys.argv)
if narg >= 2:
    filename = sys.argv[1]
else:
    filename = input('Enter filename to plot: ')

dataframe = pd.read_csv(filename)
time = np.array(dataframe.iloc[:, 0])
vehicle_speed = np.array(dataframe.iloc[:, 1])

speed = vehicle_speed / 3.6
dt = time - np.roll(time, 1)
dt[0] = dt[1]
acceleration = (np.roll(speed, -1) - np.roll(speed, 1)) / (dt + np.roll(dt, -1))  # Using central differentiation
power = ()

#---Plot
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()

ax1.plot(time, vehicle_speed, color='blue', label='Speed')
ax2.plot(time, acceleration, "g", label="Acceleration")

# Set different colors for positive and negative acceleration

ax2.fill_between(time, acceleration, where=(acceleration < 0), color='red', alpha=0.9, zorder=8)

ax1.set_xlabel(dataframe.columns[0].replace("_", " ").replace("[", " ["))
ax1.set_ylabel(dataframe.columns[1].replace("_", " ").replace("[", " ["))
ax2.set_ylabel("Deceleration - Acceleration [m/s^2]")

ax2.yaxis.label.set_color('purple')
ax2.tick_params(axis='y', colors='purple')

ax1.grid()

ax1.set_ylim((-30, 100))
ax2.set_ylim((-5, 25))

# Add legend
acceleration_legend = plt.Line2D([], [], color='green', label='Acceleration')
deceleration_legend = plt.Line2D([], [], color='red', label='Deceleration')
Speed_legend = plt.Line2D([], [], color='blue', label='Speed')
ax2.legend(handles=[acceleration_legend, deceleration_legend, Speed_legend], loc='upper left')

# Add speed on the left side
ax1.yaxis.label.set_color('blue')
ax1.tick_params(axis='y', colors='blue')

# Add time on the bottom
ax1.xaxis.label.set_color('black')
ax1.tick_params(axis='x', colors='black')

ax1.set_xlim(np.min(time), np.max(time))

plotfilename = filename.split('.')[-2] + ".png"
fig.savefig(plotfilename)

#---Kinematic analysis
print("Average speed [km/h]", np.average(vehicle_speed))
print("Max speed [km/h]", np.max(vehicle_speed))
print("Distance [m]", np.sum(speed * dt))
print("Max acceleration [m/s2]", np.max(acceleration))
print("Max deceleration [m/s2]", np.min(acceleration))

#---Energy analysis
if narg < 3:
    exit()

import json

f = open(sys.argv[2])
param = json.load(f)
f.close()

Cd = param['Aerodynamic_coefficient[-]']
Af = param['Frontal_area[m2]']
Cr = param['Rolling_resistance_coefficient[-]']
mv = param['Weight[kg]']

g = 9.81  # m/s2   gravitational acceleration
T = 298  # K    Ambient temperature
P = 101325  # Pa Ambient pressure
Ma = 0.029  # kg/mol Air molecular mass
Ru = 8.314  # J/molK Universal gas constant

rho = P * Ma / (Ru * T)

Fr = Cr * mv * g
Fa = Cd * Af * 1 / 2 * rho * speed ** 2
Ftot = mv * acceleration
Fg = 0    # gradient

Ftr = Ftot + Fr + Fa + Fg
Wtr = Ftr * speed   # W  traction power

print(np.min(Wtr), np.max(Wtr))
