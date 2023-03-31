import os
import math
import numpy as np
import tkinter as tk



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

if(len(xc)==len(yc)):
    print('são do mesmo tamanho')

# Build Figure
root = tk.Tk()
root.withdraw()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

topfig = tk.Toplevel(root, name='aeroMor')
topfig.title('aeroMorph v.5.0')
topfig.geometry(f"{1024}x{640}+{(screen_width-1024)//2}+{(screen_height-640)//2}")
topfig.config(bg='black')

frame1 = tk.Frame(topfig, bg='#d91c1c')
frame1.place(relx=0.025, rely=0.025, relwidth=0.95, relheight=0.95)

text = tk.Label(topfig, text='\u00A92008-2009 Cody Lafountain, University of Cincinnati', bg='black', fg='white', font=('Arial Unicode MS', 8), anchor='w')
text.place(x=2, y=0, width=350, height=15)

root.mainloop()




#camber_calcs function
def camber_calcs(xc, yc):
    len_xc = len(xc)
    print(type(len_xc))
    camber_line = np.zeros((39, 1))
    for i in range(int(len(xc)/2)):
    #for i in range(39):
        camber_line[i,0] = (yc[i]+yc[len(yc)-i-1])/2
    max_camber = np.max(camber_line)
    incidence_angle = np.arctan((camber_line[int(len(xc)/2-1)]-camber_line[int(len(xc)/2)])/(xc[int(len(xc)/2-1)]-xc[int(len(xc)/2)]))
    #incidence_angle = np.arctan((camber_line[int(37)]-camber_line[int(38)])/(xc[int(len(xc)/2-1)]-xc[int(len(xc)/2)]))

    incidence_angle = np.degrees(incidence_angle)
    return camber_line, max_camber, incidence_angle

nodes = [math.floor(len(xc)/2), math.floor(len(xc)*(36/80)), math.floor(len(xc)*(31/80)),
         math.floor(len(xc)*(24/80)), math.floor(len(xc)*(19/80)), math.floor(len(xc)*(15/80)),
         math.floor(len(xc)*(9/80)), 1]
xc_reset = xc
yc_reset = yc
camber_line, max_camber, incidence_angle = camber_calcs(xc, yc)
camber_line_0 = camber_line
thick = 100 * (max(yc) - min(yc))




