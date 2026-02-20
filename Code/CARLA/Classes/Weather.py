from pathlib import Path

FILE_DIR = Path(__file__).resolve().parent

from tkinter import *
from tkinter import ttk

class Weather:
    def __init__(self, client):
        self.client = client
        self.root = Tk()
        self.root.geometry("300x200")
        self._build_ui()
 
    def _build_ui(self):
        frm = ttk.Frame(self.root, padding=10)
        frm.grid()
 
        ttk.Label(frm, text="Change the Weather in Carla").grid(column=0, row=0)
 
        Label(self.root, text="Set rain intensity").grid(column=0, row=1)
        Label(self.root, text="Set wind intensity").grid(column=1, row=1)
 
        Scale(self.root, from_=0, to=100,
              orient=HORIZONTAL,
              command=self.client.set_rain).grid(column=0, row=2)
 
        Scale(self.root, from_=0, to=100,
              orient=HORIZONTAL,
              command=self.client.set_wind).grid(column=1, row=2)
 
    def run(self):
        self.root.mainloop()