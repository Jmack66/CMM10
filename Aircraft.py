import numpy as np 
import math
import vehicle as veh 
import env
from scipy import optimize
from scipy.optimize import fsolve
import CoeffecientData as cd

#EVERYTHING IS IN RADIANS GOOOOOOOOOOOOOOOD

testing = {"Velocity" : 100, "Flight Path" : 0.0, "Altitude" : -1000, "Time Step" : 0.01}

class Aircraft():
    def __init__(self, initials):
        self.z_e = initials.get("Altitude")
        self.V = initials.get("Velocity")
        self.gamma = initials.get("Flight Path")
        self.time_step = initials.get("Time Step")
        self.mass = veh.acMass # this line isnt really needed but wanted to be able to access mass with .mass
        self.weight = veh.acMass * env.gravity
        self.coeff,self.null = cd.set_coeffecients()
    def trim(self,alpha_x):
        self.delta_el = -(self.coeff.get("CM_0") + self.coeff.get("CM_alpha")*alpha_x)/self.coeff.get("CM_delta")
        return self.delta_el
    def get_CL(self,alpha_x):
        return self.coeff.get("CL_0") + self.coeff.get("CL_alpha")*alpha_x + self.coeff.get("CL_delta")*self.delta_el #for now using the class deltael variable as opposed to calling the function-- understanding is that del el doesnt change
    def get_CD(self,alpha_x):
        return self.coeff.get("CD_0") + self.coeff.get("CD_K")*self.get_CL(alpha_x)**2
    def set_theta(self,alpha_x):
        self.theta = alpha_x + self.gamma
        return self.theta
    def get_drag(self,a):
        self.Drag = 0.5 * env.air_density * self.V**2 * veh.Sref * self.get_CD(a)
        return self.Drag
    def get_lift(self,a):
        self.Lift = 0.5 * env.air_density * self.V**2 * veh.Sref * self.get_CL(a)
        return self.Lift
    def get_thrust(self,a):
        self.Thrust = self.Drag * np.cos(a) + self.weight * np.sin(self.set_theta(a)) - self.Lift * np.sin(a)
        return self.Thrust
    def get_moment(self):
        self.Moment = (env.air_density*veh.Sref*veh.cbar*self.coeff.get("CM_0")*self.V**2)/2 # are functions with a "_0" limited to only the initial conditions???? 
    def find_alpha(self,a):
        return (self.get_lift(a)* np.cos(a)) + self.get_drag(a) * np.sin(a) + self.weight * np.cos(self.set_theta(a)) #This equation does not seem to be rearranged correctly at first glance
    def get_alpha(self):
        self.alpha = optimize.fsolve(self.find_alpha,0)
        return self.alpha
    def get_ub(self,a):
        self.ub = self.V*np.cos(a)
        return self.ub
    def get_wb(self,a):
        self.wb = self.V*np.sin(a)
        return self.wb
    def get_forces(self,a): #wapper function just gets the drag,lift and moment forces in one
        self.get_drag(a)
        self.get_lift(a)
        self.get_thrust(a)
        self.get_moment(a)
    def set_initials(self):
        self.get_alpha()
        self.trim()



a = Aircraft(testing)
