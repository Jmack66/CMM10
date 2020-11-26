import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

import tkinter as tk
from tkinter import ttk
import CoeffecientData as cd 
import Simulator as sim
#Colors 
HIGHLIGHT = '#40FFB8'
BG = '#6B6B6B'
DEEP = '#505050'

LARGE_FONT= ("Verdana", 20)

#GUI Inspiration and boiler code courtesy of https://pythonprogramming.net/how-to-embed-matplotlib-graph-tkinter-gui/
"""
Some general notes-- this GUI code isnt great-- its very botched. I would love to add an option to have the control values be managed by a PID controller - Jonah
"""
class Simulator_gui(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        self.fig1 = 0
        self.fig2 = 0
        for F in (StartPage, PageOne, PageTwo, PageThree):

            frame = F(container, self)

            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="NSEW")
            frame.configure(bg = BG)

        self.show_frame(StartPage)
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
    def results(self,fig,fig2):
        PageThree.fig1 = fig
        PageThree.fig2 = fig2
        PageThree.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        def setSimVars(self,velocity,angle,runtime,el_change,el_time,thrust_change,thrust_time):
            user_vel = velocity.get()
            user_ang = angle.get()
            user_run_time = runtime.get()
            user_el_change = el_change.get()
            user_el_time = el_time.get()
            user_thrust_change = thrust_change.get()
            user_thrust_time = thrust_time.get()
            try:
                user_vel = int(user_vel)
                user_ang = int(user_ang)
                user_run_time = int(user_run_time)
                user_el_change = int(user_el_change)
                user_el_time = int(user_el_time)
                user_thrust_change = int(user_thrust_change)
                user_thrust_time = int(user_thrust_time)
                error = tk.Label(self, text="-------Simulation parameters set-------", fg = HIGHLIGHT ,bg = BG, font= ("Verdana", 8)).grid(row = 13,column = 2)
            except (ValueError,TypeError):
                try:
                    user_vel = float(user_vel)
                    user_ang = float(user_ang)
                    user_run_time = float(user_run_time)
                    user_el_change = float(user_run_time)
                    user_el_time = float(user_el_time)
                    user_thrust_change = float(user_thrust_change)
                    user_thrust_time = float(user_thrust_time)
                    error = tk.Label(self, text="-------Simulation parameters set-------", fg = HIGHLIGHT ,bg = BG, font= ("Verdana", 8)).grid(row = 13,column = 2)
                except ValueError:
                    error = tk.Label(self, text="ENTER FLOAT OR INTEGER VALUE", fg = '#FF0000',bg = BG, font= ("Verdana", 8)).grid(row = 13,column = 2)
            self.sim_vars = {"Velocity" : user_vel, "Flight Path" : user_ang, "Run Time" : user_run_time, "Elevator Change" : user_el_change, "Elevator Time" : user_el_time, "Thrust Change" : user_thrust_change, "Thrust Time" :user_thrust_time}
            return 0
        def run_simulation(self):
            simp = sim.Simulator(self.sim_vars)
            simp.set_initials()
            self.fig, self.fig2 = simp.cycles()
            return True 
        def show_plots(self):
            self.fig
            self.fig2
            plt.show()
        tk.Frame.__init__(self,parent)
        title = tk.Label(self, text="Aircraft Properties", fg = HIGHLIGHT,bg = BG, font=LARGE_FONT).grid(row = 0,column = 2)
        logo = tk.PhotoImage(file="logo.png") 
        img = tk.Label(self, image = logo)
        img.image = logo
        img.grid(row = 1, column = 2)
        tk.Label(self,fg =HIGHLIGHT ,bg = BG, text="Velocity(m/s): ", font=("Verdana", 15)).grid(row = 3,column = 1)
        tk.Label(self,fg = HIGHLIGHT,bg = BG, text="Flight Angle(deg): ",font=("Verdana", 15)).grid(row = 4,column = 1)
        tk.Label(self,fg = HIGHLIGHT,bg = BG, text="Simulation Run Time(s): ",font=("Verdana", 15)).grid(row = 5,column = 1)
        tk.Label(self,fg = HIGHLIGHT,bg = BG, text="Percentage elevator change(%): ",font=("Verdana", 15)).grid(row = 6,column = 1)
        tk.Label(self,fg = HIGHLIGHT,bg = BG, text="Time of elevator change(s): ",font=("Verdana", 15)).grid(row = 7,column = 1)
        tk.Label(self,fg = HIGHLIGHT,bg = BG, text="Percentage thrust change(%): ",font=("Verdana", 15)).grid(row = 9,column = 1)
        tk.Label(self,fg = HIGHLIGHT,bg = BG, text="Time of thrust change(s): ",font=("Verdana", 15)).grid(row = 10,column = 1)
        tk.Label(self, text="", fg = '#FF0000',bg = BG, font= ("Verdana", 6))
        velocity = tk.Entry(self, width=20,fg = HIGHLIGHT,bg = DEEP)
        velocity.grid(row = 3,column = 2)
        angle = tk.Entry(self, width=20,fg = HIGHLIGHT,bg = DEEP)
        angle.grid(row = 4,column = 2)
        runtime = tk.Entry(self, width=20,fg = HIGHLIGHT,bg = DEEP)
        runtime.grid(row = 5,column = 2)
        el_change = tk.Entry(self, width=20,fg = HIGHLIGHT,bg = DEEP)
        el_change.grid(row = 6,column = 2)
        el_time = tk.Entry(self, width=20,fg = HIGHLIGHT,bg = DEEP)
        el_time.grid(row = 7,column = 2)
        thrust_change = tk.Entry(self, width=20,fg = HIGHLIGHT,bg = DEEP)
        thrust_change.grid(row = 9,column = 2)
        thrust_time = tk.Entry(self, width=20,fg = HIGHLIGHT,bg = DEEP)
        thrust_time.grid(row = 10,column = 2)
        confirm = tk.Button(self, text="Confirm Properties",fg = HIGHLIGHT,bg = BG,
                            command=lambda: setSimVars(self,velocity,angle,runtime,el_change,el_time,thrust_change,thrust_time)).grid(row = 14, column = 1)
        run = tk.Button(self, text="Run",fg = HIGHLIGHT,bg = BG,
                            command=lambda: run_simulation(self)).grid(row = 14, column = 2)

        button3 = tk.Button(self, text="Future functionality",fg = HIGHLIGHT,bg = BG,
                            command=lambda: show_plots).grid(row = 14, column = 5)

class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page One!!!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = ttk.Button(self, text="Page Two",
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack()


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page Two!!!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = ttk.Button(self, text="Page One",
                            command=lambda: controller.show_frame(PageOne))
        button2.pack()


class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Graph Page!",bg = BG, fg = HIGHLIGHT, font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = tk.Button(self, text="Back to Home",fg = HIGHLIGHT,bg = BG,
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()
   
        

    def data_handler(self):
        #data go
        return True
