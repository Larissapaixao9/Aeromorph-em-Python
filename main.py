import os
import math
import numpy as np
import tkinter as tk
from tkinter import ttk 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
# import Ipython
# from IPython.display import clear_output

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

def plotter(canvas, xc, yc, xc_reset, yc_reset, camber_line, nodes, camber_line_0):
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

    # Embed the Matplotlib figure in the Tkinter canvas
    canvas = FigureCanvasTkAgg(fig, master=canvas)
    canvas.draw()
    canvas.get_tk_widget().pack()

#######################
def getnode(event):
    node = int(node_select.get()) - 1
    displacement = yc[nodes[node]] - yc_reset[nodes[node]]
    node_displacement.config(text=str(displacement))
    get_node_y = yc[nodes[node]]
    node_value.config(text=str(get_node_y))
#######################

def topcurvefit(fit_line_button, eventdata):
    global xc, yc, xc_reset, yc_reset, camber_value, incidence_value, thickness_value, node_select, node_displacement

    x_unfit = xc[:int(len(xc)/2)+1]
    y_unfit = yc[:int(len(xc)/2)+1]
    power = 18
    p = np.polyfit(x_unfit, y_unfit, power)
    
    y_fit = np.zeros(len(x_unfit))
    for i in range(len(x_unfit)):
        y = np.zeros(power)
        y[0] = p[0] * x_unfit[i]**power
        for j in range(2, power+1):
            y[j-1] = y[j-2] + p[j-1] * x_unfit[i]**(power-j+1)
        y_fit[i] = y[power-1] + p[power]
        
    yc[:int(len(xc)/2)+1] = y_fit[:len(y_fit)]
    
    camber_line, max_camber, incidence_angle = camber_calcs(xc, yc)
    incidence_value.config(text=str(incidence_angle))
    camber_value.config(text=str(max_camber))
    thickness_value.config(text=str(100*(max(yc)-min(yc))))
    
    node = node_select.current()
    displacement = yc[nodes[node]] - yc_reset[nodes[node]]
    node_displacement.config(text=str(displacement))
    
    plotter(canvas,xc, yc, xc_reset, yc_reset, camber_line, nodes, camber_line_0)
    write_log('smoo')


def setnode(node_edit, event):
    global xc, yc, nodes
    point1xn = []
    point1y = []
    point2x = []
    point2y = []
    val = node_edit.get()
    node = node_select.get()
    # Change Node
    if val == '1':
        ychange = 0
    elif val == '2':
        ychange = 0.025
    elif val == '3':
        ychange = 0.01
    elif val == '4':
        ychange = 0.005
    elif val == '5':
        ychange = -0.005
    elif val == '6':
        ychange = -0.01
    elif val == '7':
        ychange = -0.025
    if node == 1 or node == 8:
        print('Endpoints cannot be changed')
    elif node == 2 or node == 3 or node == 4 or node == 5 or node == 6 or node == 7:
        yc[nodes[node-1]+1:nodes[node]] = yc[nodes[node-1]+1:nodes[node]] + ychange
        # left panel
        point1x = xc[nodes[node-1]:nodes[node]-1]
        point1y = yc[nodes[node-1]:nodes[node]-1]
        xpoint1 = -point1x[-1] + point1x[0]
        ypoint1 = -point1y[-1] + point1y[0]
        thetachange1 = math.atan((ychange+ypoint1)/xpoint1) - math.atan(ypoint1/xpoint1)
        thetaold1 = np.array([math.atan(x) for x in point1y/point1x])
        theta1 = thetachange1 + thetaold1
        rad1x1 = np.array([math.sqrt(x**2 + y**2)/math.cos(thetachange1) for x, y in zip(point1x, point1y)])
        xnew1 = rad1x1 * np.cos(theta1)
        ynew1 = rad1x1 * np.sin(theta1)
        xnew11 = xnew1 + (point1x[-1] - xnew1[-1])
        ynew11 = ynew1 + (point1y[-1] - ynew1[-1])
        for i in range(len(point1x)):
            xc[i+nodes[node-1]] = xnew11[i]
            yc[i+nodes[node-1]] = ynew11[i]
        # right panel
        interval = list(range(nodes[node], nodes[node+1]))
        point2x = xc[interval]
        point2y = yc[interval]
        xpoint2 = point2x[-1] - point2x[0]
        ypoint2 = point2y[-1] - point2y[0]
        thetachange2 = math.atan((ychange+ypoint2)/xpoint2) - math.atan(ypoint2/xpoint2)
        thetaold2 = np.array([math.atan(x) for x in point2y/point2x])
        theta2 = thetaold2 + thetachange2
        rad1x2 = np.array([math.sqrt(x**2 + y**2)/math.cos(thetachange2) for x, y in zip(point2x, point2y)])
        xnew2 = rad1x2 * np.cos(theta2)
    ####################################
def set_thickness(thickness_edit, eventdata):
        val = thickness_edit.get()
        if val == 1:
            thickness_change = 0
        elif val == 2:
            thickness_change = 0.04
        elif val == 3:
            thickness_change = 0.02
        elif val == 4:
            thickness_change = 0.01
        elif val == 5:
            thickness_change = -0.01
        elif val == 6:
            thickness_change = -0.02
        elif val == 7:
            thickness_change = -0.04
        set_thickness2(thickness_change)
#######################################
  

def set_thickness2(thickness_change):
    node = node_select.get_value()
    for i in range(1, len(yc)//2):
        thickness = yc[i] - yc[len(yc)-i]
        thick_change = (thickness / max(thickness)) * 0
        yc[i] += thick_change
    for i in range(1, len(yc)//2):
        thickness = yc[i] - yc[len(yc)-i]
        thick_change = (thickness / max(thickness)) * thickness_change
        yc[i] += thick_change
    camber_line, max_camber, incidence_angle = camber_calcs(xc, yc)
    incidence_value.set_string(str(incidence_angle))
    camber_value.set_string(str(max_camber))
    node_value.set_string(str(yc[nodes[node]]))
    thickness_value.set_string(str(100*(max(yc)-min(yc))))
    node = node_select.get_value()
    displacement = yc[nodes[node]] - yc_reset[nodes[node]]
    node_displacement.set_string(str(displacement))
    filename_edit.set_string(filename_load.get_string() + '-AM' + '-t' + str(round(float(thickness_value.get_string()))) + '-s' + sweep_value.get_string())
    plotter(xc, yc, xc_reset, yc_reset, camber_line, nodes, camber_line_0)
    write_log('topt')
#################################

def reset_airfoil(reset_button, event):
    global xc, yc
    xc = xc_reset.copy()
    yc = yc_reset.copy()
    camber_line, max_camber, incidence_angle = camber_calcs(xc, yc)
    incidence_value.config(text=str(incidence_angle))
    camber_value.config(text=str(max_camber))
    thickness_value.config(text=str(100*(max(yc)-min(yc))))
    node = node_select.get()
    displacement = yc[nodes[node]] - yc_reset[nodes[node]]
    node_displacement.config(text=str(displacement))
    filename_edit.config(text=filename_load.get() + '-AM')
    sweep_value.config(text='0')
    plotter(canvas, xc, yc, xc_reset, yc_reset, camber_line, nodes, camber_line_0)
    write_log('rese')
    print('\n')
###############################

def exit_editor(exit_button, event):
    plt.close('all')
    plt.clf()
    plt.cla()
    plt.close()
    clear_output(wait=True)
    print('\n\nExiting editor...')
###############################


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
root.iconify()  # minimize the root window
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

plotter(plot1, xc, yc, xc_reset, yc_reset, camber_line, nodes, camber_line_0)

# # Show the main window and start the event loop
# root.deiconify()
# topfig.mainloop()


# Check if topfig still exists before creating subframes
if topfig.winfo_exists():
    # Build editor
    subframe2 = tk.Frame(frame1, bg="white", bd=2, relief="groove")
    subframe2.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

    subframe3 = tk.Frame(frame1, bg="white", bd=2, relief="groove")
    subframe3.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

    # Data Box
    tk.Label(subframe3, text="Node YValue", font=("Arial UnicodeMS", 10, "bold"), anchor="w").place(x=10, y=225)
    node_value = tk.Label(subframe3, text="0")
    node_value.place(x=10, y=205)

    
tk.Label(subframe3, text="NodeDisplacement", font=("Arial UnicodeMS", 10, "bold"), anchor="w").grid(row=1, column=0, padx=10, pady=10, sticky="w")
node_displacement = tk.Label(subframe3, text="0")
node_displacement.grid(row=1, column=1, padx=10, pady=10, sticky="w")

tk.Label(subframe3, text="Thickness%", font=("Arial UnicodeMS", 8, "bold"), anchor="w").grid(row=2, column=0, padx=10, pady=10, sticky="w")
thickness_value = tk.Label(subframe3, text=str(thick))
thickness_value.grid(row=2, column=1, padx=10, pady=10, sticky="w")

tk.Label(subframe3, text="MaxCamber", font=("Arial UnicodeMS", 8, "bold"), anchor="w").grid(row=3, column=0, padx=10, pady=10, sticky="w")
camber_value = tk.Label(subframe3, text=str(max_camber))
camber_value.grid(row=3, column=1, padx=10, pady=10, sticky="w")

tk.Label(subframe3, text="SweepAngle", font=("Arial UnicodeMS", 8, "bold"), anchor="w").grid(row=4, column=0, padx=10, pady=10, sticky="w")
sweep_value = tk.Label(subframe3, text="0")
sweep_value.grid(row=4, column=1, padx=10, pady=10, sticky="w")

tk.Label(subframe3, text="IncidenceAngle", font=("Arial UnicodeMS", 8, "bold"), anchor="w").grid(row=5, column=0, padx=10, pady=10, sticky="w")
incidence_value = tk.Label(subframe3, text=str(incidence_angle))
incidence_value.grid(row=5, column=1, padx=10, pady=10, sticky="w")

# Column 1
tk.Label(subframe2, text="SelectNode", font=("Arial UnicodeMS", 8, "bold"), bg="white").place(x=10, y=190)
node_select = ttk.Combobox(subframe2, values=["1", "2", "3", "4", "5", "6", "7", "8"])
node_select.current(0)
node_select.place(x=10, y=170)
node_select.bind("<<ComboboxSelected>>", getnode)

tk.Label(subframe2, text="Raise/LowerNode", font=("Arial UnicodeMS", 8, "bold"), bg="white").place(x=10, y=150)
node_edit = ttk.Combobox(subframe2, values=["0", "+0.025", "+0.01", "+0.005", "-0.005", "-0.01", "-0.025"])
node_edit.current(0)
node_edit.place(x=10, y=130)
node_edit.bind("<<ComboboxSelected>>", setnode)

tk.Label(subframe2, text="ThicknessChange", font=("Arial UnicodeMS", 8, "bold"), bg="white").place(x=10, y=110)
thickness_edit = ttk.Combobox(subframe2, values=["0", "+4%", "+2%", "+1%", "-1%", "-2%", "-4%"])
thickness_edit.current(0)
thickness_edit.place(x=10, y=90)
thickness_edit.bind("<<ComboboxSelected>>", set_thickness)

fit_line_button = tk.Button(subframe2, text="Smooth Surface", font=("Arial UnicodeMS", 8, "bold"), bg="#CCCCCC", command=topcurvefit)
fit_line_button.place(x=10, y=50)

reset_button = tk.Button(subframe2, text="Reset Airfoil", font=("Arial UnicodeMS", 10, "bold"), bg="#CCCCCC", command=reset_airfoil)
reset_button.place(x=10, y=30)

exit_button = tk.Button(subframe2, text="Exit Editor", font=("Arial UnicodeMS", 10, "bold"), bg="#CCCCCC", command=exit_editor)
exit_button.place(x=10, y=10)
root.deiconify()
topfig.mainloop()