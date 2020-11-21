import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

import tkinter as tk
from tkinter import ttk
import CoeffecientData as cd 
import AircraftDynamics 

#Colors 
HIGHLIGHT = '#40FFB8'
BG = '#6B6B6B'
DEEP = '#505050'

LARGE_FONT= ("Verdana", 20)

#GUI Inspiration and boiler code courtesy of https://pythonprogramming.net/how-to-embed-matplotlib-graph-tkinter-gui/


class Simulator(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)

        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo, PageThree):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="NSEW")
            frame.configure(bg = BG)

        self.show_frame(StartPage)
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()




class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        def setSimVars(self,velocity,angle):
            user_vel = velocity.get()
            user_ang = angle.get()
            try:
                val = int(user_vel)
                val2 = int(user_ang)
                error = tk.Label(self, text="-------Simulation parameters set-------", fg = HIGHLIGHT ,bg = BG, font= ("Verdana", 8)).grid(row = 5,column = 2)
            except (ValueError,TypeError):
                try:
                    val = float(user_vel)
                    val2 = float(user_ang)
                    error = tk.Label(self, text="-------Simulation parameters set-------", fg = HIGHLIGHT ,bg = BG, font= ("Verdana", 8)).grid(row = 5,column = 2)
                except ValueError:
                    error = tk.Label(self, text="ENTER FLOAT OR INTEGER VALUE", fg = '#FF0000',bg = BG, font= ("Verdana", 8)).grid(row = 5,column = 2)
                    
        tk.Frame.__init__(self,parent)
        title = tk.Label(self, text="Aircraft Properties", fg = HIGHLIGHT,bg = BG, font=LARGE_FONT).grid(row = 0,column = 2)
        logo = tk.PhotoImage(file="logo.png") 
        img = tk.Label(self, image = logo)
        img.image = logo
        img.grid(row = 1, column = 2)
        vel_label = tk.Label(self,fg =HIGHLIGHT ,bg = BG, text="Velocity(m/s): ", font=("Verdana", 15)).grid(row = 3,column = 1)
        angle_label = tk.Label(self,fg = HIGHLIGHT,bg = BG, text="Flight Angle(deg): ",font=("Verdana", 15)).grid(row = 4,column = 1)
        error = tk.Label(self, text="", fg = '#FF0000',bg = BG, font= ("Verdana", 6))
        velocity = tk.Entry(self, width=20,fg = HIGHLIGHT,bg = DEEP)
        velocity.grid(row = 3,column = 2)
        angle = tk.Entry(self, width=20,fg = HIGHLIGHT,bg = DEEP)
        angle.grid(row = 4,column = 2)
        confirm = tk.Button(self, text="Confirm Properties",fg = HIGHLIGHT,bg = BG,
                            command=lambda: setSimVars(self,velocity,angle)).grid(row = 6, column = 2)

        button = tk.Button(self, text="Visit Page 1",fg = HIGHLIGHT,bg = BG,
                            command=lambda: controller.show_frame(PageOne)).grid(row = 7, column = 3)
        button2 = tk.Button(self, text="Visit Page 2",fg = HIGHLIGHT,bg = BG,
                            command=lambda: controller.show_frame(PageTwo)).grid(row = 7, column = 4)

        button3 = tk.Button(self, text="Coeffecient Curves",fg = HIGHLIGHT,bg = BG,
                            command=lambda: controller.show_frame(PageThree)).grid(row = 7, column = 5)

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
        self.data_handler()
        f = self.fig1
        f2 = self.fig2
        
        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        canvas = FigureCanvasTkAgg(f2, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def data_handler(self):
        cd.set_coeffecients()
        self.fig1,self.fig2 = cd.getPlots()
        return True

app = Simulator()
app.mainloop()