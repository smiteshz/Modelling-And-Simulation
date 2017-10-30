import numpy as np
import tkinter as tk
"""This file will create a GUI environment built using Tkinter. It will also be responsible for the behaviour of the cars
in the scene."""
# STATE = [][]
# CARS = [][[]]
GRID = list([[20],[20]])

#The driver program will give input to this environment and the environment will give feedback to the driver program
#Types of input events from the driver program
#Car[index=a,occupied=True/False,n_seats = 1 to 6,passengers=[],Position=[x,y]], a is the car index, updates car position on MAP
#Spwn_Pgr[index = a, number of passsengers = b, carpool=True/False ,spawn_position=[x,y]] updates passenger position on MAP and returns grid position of all the cars
#Occupy[passindex = a,carindex = b] updates the state of the passenger and car to change to occupied and delete the passenger visibility on the MAP
#DropOff[passindex = a,carindex = b] updates the state of the car and destroyes the passenger object. Also saves the trip information in the telemetry matrix

"""Render function the redraw the graphic according to the current state"""

def create_grid(c,w,h):
	#w = c.winfo_width() # Get current width of canvas
	#h = c.winfo_height() # Get current height of canvas
	#c.delete('grid_line') # Will only remove the grid_line
    # Creates all vertical lines at intevals of 100
	for i in range(0, w, int(w/10)):
		c.create_line([(i, 0), (i, h)], tag='grid_line')

    # Creates all horizontal lines at intevals of 100
	for i in range(0, h, int(h/10)):
		c.create_line([(0, i), (w, i)], tag='grid_line')

def update_data(c,cars=np.array([[]]),passengers = np.array([[]])):
	w = 500#c.winfo_width()
	h = 500#c.winfo_height()
	try:
		for i in cars:
			print(w,h,i[0],i[1])
			c.create_oval(i[0]*(w/10)+1,i[0]*(w/10)+1,i[1]*(h/10)-1,i[1]*(h/10)-1,outline="#f00",fill="#0f0",width=2)
		# for i in passengers:
		# 	c.create_oval((i[0]*10*w,i[1]*10*h),20,20,outline="#f00",fill="#00f",width=2)
	except IndexError:
		print("Itsokay")

root = tk.Tk()

c = tk.Canvas(root, height=500, width=500, bg='white')
c.pack(fill=tk.BOTH, expand=True)
#create_grid(cars=np.array([[1,2],[2,3]]))
create_grid(c,500,500)
a = np.array(([[3,2]]))
b = np.array(([[10,9]]))
update_data(c,cars=a,passengers=b)
root.mainloop()

