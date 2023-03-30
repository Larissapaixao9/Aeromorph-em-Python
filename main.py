import os
import math


camber_line=0;camber_line_0=0;camber_value=0;incidence_value=0
nodes=0;node_displacement=0;node_select=0;node_value=0; thickness_value=0;xc=0
xc_reset=0;yc=0;yc_reset=0;ga_progress=0;ga_total=0

# Add all filepaths
dir_path = os.getcwd()
airfoildir = os.path.join(dir_path, 'airfoils')
helpdir = os.path.join(dir_path, 'help')

# Load Airfoil
inputfile = os.path.join(airfoildir, 'lrn1015.dat')
with open(inputfile, 'r') as file:
    data = file.readlines()
xc, yc = [], []
for line in data:
    x, y = line.split()
    xc.append(float(x))
    yc.append(float(y))

print(xc)

