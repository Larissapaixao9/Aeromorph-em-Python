import os
import math
import numpy as np
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure



camber_line=0;camber_line_0=0;camber_value=0;incidence_value=0
nodes=0;node_displacement=0;node_select=0;node_value=0; thickness_value=0;xc=0
xc_reset=0;yc=0;yc_reset=0;ga_progress=0;ga_total=0


#camber_calcs function
def camber_calcs(xc, yc):
    camber_line = []
    for i in range(len(xc)//2):
        camber_line.append((yc[i] + yc[len(yc)-i-1]) / 2)
    max_camber = max(camber_line)
    incidence_angle = np.arctan((camber_line[len(xc)//2-1] - camber_line[len(xc)//2-1]) / (xc[len(xc)//2-1] - xc[len(xc)//2])) * 180/np.pi
    #incidence_angle = np.arctan((camber_line[len(xc)//2-1] - camber_line[len(xc)//2]) / (xc[len(xc)//2-1] - xc[len(xc)//2])) * 180/np.pi
    return camber_line, max_camber, incidence_angle

def plotter(xc, yc, xc_reset, yc_reset, camber_line, nodes, camber_line_0):
    # Create a new tkinter window
    topfig = tk.Toplevel()

    # Create a new Matplotlib figure
    fig = Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot(111)

    # Plot the data on the Matplotlib figure
    ax.fill(xc_reset, yc_reset, [.8, .8, .8])
    ax.plot(xc, yc, '--k')
    for node in nodes:
        ax.plot(xc[node], yc[node], 'ko')
    ax.plot(xc[:len(xc)//2], camber_line_0[:len(xc)//2], '-b')
    ax.plot(xc[:len(xc)//2], camber_line, '--b')
    ax.axis([0, 1, -.125, .225])

    # Embed the Matplotlib figure in the tkinter window
    canvas = FigureCanvasTkAgg(fig, master=topfig)
    canvas.draw()
    canvas.get_tk_widget().pack()

    # Show the tkinter window
    topfig.mainloop()

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

xc_reset = xc.copy()
yc_reset = yc.copy()

nodes = [math.floor(len(xc)/2), math.floor(len(xc)*(36/80)), math.floor(len(xc)*(31/80)),
         math.floor(len(xc)*(24/80)), math.floor(len(xc)*(19/80)), math.floor(len(xc)*(15/80)),
         math.floor(len(xc)*(9/80)), 1]
# nodes = [int(math.floor(len(xc)/2)), int(math.floor(len(xc)*(36/80))), int(math.floor(len(xc)*(31/80))),
#          int(math.floor(len(xc)*(24/80))), int(math.floor(len(xc)*(19/80))), int(math.floor(len(xc)*(15/80))),
#          int(math.floor(len(xc)*(9/80))), 1]

camber_line, max_camber, incidence_angle = camber_calcs(xc, yc)
camber_line_0 = camber_line
thick = 100 * (max(yc) - min(yc))




#Build Figure

# Set screen size
root = tk.Tk()
root.withdraw()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Build main window
topfig = tk.Toplevel()
topfig.title("AeroMorph v.5.0")
topfig.geometry(f"1024x640+{(screen_width-1024)//2}+{(screen_height-640)//2}")
topfig.config(bg="black")
topfig.resizable(False, False)

frame1 = tk.Frame(topfig, bg="pink")
frame1.place(relx=0.025, rely=0.025, relwidth=0.95, relheight=0.95)

tk.Label(frame1, text="©2008-2009 Cody Lafountain, University of Cincinnati", bg="black", fg="white", anchor="w", font=("Arial UnicodeMS", 8, "bold")).place(x=2, y=0)

# Build plot
plot1 = tk.Canvas(frame1, bg="white")
plot1.place(relx=0.04, rely=0.05, relwidth=0.95, relheight=0.5)

plotter(xc, yc, xc_reset, yc_reset, camber_line, nodes, camber_line_0)

# Build editor
subframe2 = tk.Frame(frame1, bg="white", bd=2, relief="groove")
subframe2.place(relx=0.04, rely=0.56, relwidth=0.76, relheight=0.43)

subframe3 = tk.Frame(frame1, bg="white", bd=2, relief="groove")
subframe3.place(relx=0.80, rely=0.56, relwidth=0.19, relheight=0.43)

# Data Box
tk.Label(subframe3, text="Node YValue", font="@Arial Unicode MS 10 bold", anchor="w").place(x=10, y=225)
node_value = tk.Label(subframe3, text="0")
node_value.place(x=10, y=205)

tk.Label(subframe3, text="NodeDisplacement", font="@Arial Unicode MS 10 bold", anchor="w").place(x=10, y=185)
node_displacement = tk.Label(subframe3, text="0")
node_displacement.place(x=10, y=165)

tk.Label(subframe3, text="Thickness%", font="@Arial Unicode MS 10 bold", anchor="w").place(x=10, y=145)
thickness_value = tk.Label(subframe3, text=str(thick))
thickness_value.place(x=10, y=125)

tk.Label(subframe3, text="MaxCamber", font="@Arial Unicode MS 10 bold", anchor="w").place(x=10, y=105)
camber_value = tk.Label(subframe3, text=str(max_camber))
camber_value.place(x=10, y=85)

tk.Label(subframe3, text="SweepAngle", font="@Arial Unicode MS 10 bold", anchor="w").place(x=10, y=65)
sweep_value = tk.Label(subframe3, text="0")
sweep_value.place(x=10, y=45)

tk.Label(subframe3, text="IncidenceAngle", font="@Arial Unicode MS 10 bold", anchor="w").place(x=10, y=25)
incidence_value = tk.Label(subframe3, text=str(incidence_angle))
incidence_value.place(x=10, y=5)
