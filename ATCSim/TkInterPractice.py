from tkinter import *
import random
import time

tk = Tk()
canvas = Canvas(tk, width = 500, height = 400)
tk.title("Drawing")
canvas.pack()

ball = canvas.create_oval(10,10,60,60, fill = "orange")

xspeed = 1
yspeed = 2

while True:
    time.sleep(0.01)
    canvas.move(ball, xspeed, yspeed)
    tk.update()

tk.mainloop()