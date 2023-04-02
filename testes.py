import os
import math
import numpy as np

camber_line=0;camber_line_0=0;camber_value=0;incidence_value=0
nodes=0;node_displacement=0;node_select=0;node_value=0; thickness_value=0;xc=0
xc_reset=0;yc=0;yc_reset=0;ga_progress=0;ga_total=0

current_dir = os.getcwd()
airfoildir = os.path.join(current_dir, 'airfoils')
helpdir = os.path.join(current_dir, 'help')


def camber_calcs(xc, yc):
    camber_line = []
    for i in range(len(xc)//2):
        camber_line.append((yc[i] + yc[len(yc)-i-1]) / 2)
    max_camber = max(camber_line)
    
    print(camber_line[len(xc)//2-1])
    
    incidence_angle = np.arctan((camber_line[len(xc)//2-1] - camber_line[len(xc)//2-1]) / (xc[len(xc)//2-1] - xc[len(xc)//2])) * 180/np.pi
    return camber_line, max_camber, incidence_angle

# Load Airfoil
airfoildir = os.path.join(current_dir, 'airfoils')
inputfile = os.path.join(airfoildir, 'lrn1015.dat')
with open(inputfile) as f:
    data = np.loadtxt(f)
xc = data[:, 0]
yc = data[:, 1]

nodes = [math.floor(len(xc)/2), math.floor(len(xc)*(36/80)), math.floor(len(xc)*(31/80)),
         math.floor(len(xc)*(24/80)), math.floor(len(xc)*(19/80)), math.floor(len(xc)*(15/80)),
         math.floor(len(xc)*(9/80)), 1]

camber_line, max_camber, incidence_angle = camber_calcs(xc, yc)
