import numpy as np 
import math
import vehicle as veh 
import env
from scipy import optimize
from scipy.optimize import fsolve
import CoeffecientData as cd

#EVERYTHING IS IN RADIANS GOOOOOOOOOOOOOOOD

testing = {"Velocity" : 80, "Flight Path" : 0.0, "Altitude" : -1000, "Time Step" : 0.01}

class Aircraft():
    def __init__(self, initials):
        self.z_e = initials.get("Altitude")
        self.V = initials.get("Velocity")
        self.gamma = initials.get("Flight Path")
        self.time_step = initials.get("Time Step")
        self.mass = veh.acMass # this line isnt really needed but wanted to be able to access mass with .mass
        self.weight = veh.acMass * env.gravity
        self.coeff,self.null = cd.set_coeffecients()
    def trim(self,a):#alpha in is radians
        self.delta_el = -(self.coeff.get("CM_0") + self.coeff.get("CM_alpha")*np.degrees(a))/self.coeff.get("CM_delta")
        return self.delta_el
    def get_CL(self,a):#alpha in is radians
        return self.coeff.get("CL_0") + self.coeff.get("CL_alpha")*np.degrees(a) + self.coeff.get("CL_delta")*self.trim(a) #for now using the class deltael variable as opposed to calling the function-- understanding is that del el doesnt change
    def get_CD(self,a):#alpha in radians
        return self.coeff.get("CD_0") + self.coeff.get("CD_K")*self.get_CL(a)**2
    def get_CM(self,a):
        return self.coeff.get("CM_0")+(self.coeff.get("CM_alpha")*np.degrees(a))+(self.coeff.get("CM_delta")*self.trim(a))
    def set_theta(self,a): #alpha in rads
        self.theta = a + self.gamma
        return self.theta #theta in rads
    def get_drag(self,a):
        self.Drag = 0.5 * env.air_density * self.V**2 * veh.Sref * self.get_CD(a)
        return self.Drag
    def get_lift(self,a):
        self.Lift = 0.5 * env.air_density * self.V**2 * veh.Sref * self.get_CL(a)
        return self.Lift
    def get_thrust(self,a):
        self.Thrust = self.Drag * np.cos(math.radians(a)) + self.weight * np.sin(self.set_theta(math.radians(a))) - self.Lift * np.sin(math.radians(a))
        return self.Thrust
    def get_moment(self,a):
        self.Moment = (env.air_density*veh.Sref*veh.cbar*self.get_CM(a)*self.V**2)/2
    def find_alpha(self,alpha_rad):
        return (0.5 * env.air_density * self.V**2 * veh.Sref) * (self.get_CL(alpha_rad) * np.cos(alpha_rad) + self.get_CD(alpha_rad) * np.sin(alpha_rad)) - self.weight * np.cos(self.set_theta(alpha_rad))
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
        self.get_ub(a)
        self.get_wb(a)
    def set_initials(self):
        self.get_alpha()
        self.trim(self.alpha)
        self.get_forces(self.alpha)
        print(self.alpha,np.radians(self.delta_el))



a = Aircraft(testing)
a.set_initials()