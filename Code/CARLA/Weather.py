from pathlib import Path

FILE_DIR = Path(__file__).resolve().parent

from Classes import *
from tkinter import *
from tkinter import ttk

if __name__ == '__main__':
    client = CarlaClient('localhost', 2000, 10.0)
    root = Tk()
    root.geometry("300x200")
    frm = ttk.Frame(root, padding=10)
    frm.grid()
    ttk.Label(frm, text="Change the Weather in Carla").grid(column=0, row=0)
    rain_label = Label(root, text="Set rain intensity").grid(column=0, row=1)
    wind_label = Label(root, text="Set wind intensity").grid(column=1, row=1)
    rain_slider = Scale(root, from_=0, to=100, orient=HORIZONTAL, command=client.set_rain).grid(column=0, row=2)
    wind_slider = Scale(root, from_=0, to=100, orient=HORIZONTAL, command=client.set_wind).grid(column=1, row=2)
    root.mainloop()