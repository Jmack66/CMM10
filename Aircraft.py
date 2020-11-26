import numpy as np 
import math
import vehicle as veh 
import env
from scipy import optimize
from scipy.optimize import fsolve
import CoeffecientData as cd

class Aircraft():
    def __init__(self, initials):
        self.z_e = -1000
        self.V = initials.get("Velocity")
        self.gamma = initials.get("Flight Path")
        self.time_step = initials.get("Time Step")
        self.Thrust = initials.get("Thrust")
        self.mass = veh.acMass # this line isnt really needed but wanted to be able to access mass with .mass
        self.x_e = 0
        self.weight = veh.acMass * env.gravity
        self.del_mod = 1.0
        self.Thrust_mod = 1.0
        self.coeff,self.null = cd.set_coeffecients()
        self.q = 0.0
        self.delta_el = 0.0
    def trim(self,a):#alpha in is radians
        self.delta_el = -(self.coeff.get("CM_0") + self.coeff.get("CM_alpha")*np.degrees(a))/self.coeff.get("CM_delta")
        return self.delta_el
    def get_CL(self,a):#alpha in is radians
        return self.coeff.get("CL_0") + self.coeff.get("CL_alpha")*np.degrees(a) + self.coeff.get("CL_delta")*math.degrees(self.delta_el * self.del_mod) #for now using the class deltael variable as opposed to calling the function-- understanding is that del el doesnt change
    def get_CL_alpha(self,a):#alpha in is radians
        return self.coeff.get("CL_0") + self.coeff.get("CL_alpha")*np.degrees(a) + self.coeff.get("CL_delta")*self.trim(a)
    def get_CD_alpha(self,a):#alpha in radians
        return self.coeff.get("CD_0") + self.coeff.get("CD_K")*self.get_CL_alpha(a)**2
    def get_CD(self,a):#alpha in radians
        return self.coeff.get("CD_0") + self.coeff.get("CD_K")*self.get_CL(a)**2
    def get_CM(self,a):
        return self.coeff.get("CM_0")+(self.coeff.get("CM_alpha")*np.degrees(a))+(self.coeff.get("CM_delta")*math.degrees(self.delta_el * self.del_mod))
    def set_theta(self,a): #alpha in rads
        self.theta = a + self.gamma
        return self.theta #theta in rads
    def get_drag(self,a):
        self.Drag = 0.5 * env.air_density * self.V**2 * veh.Sref * self.get_CD(a)
        return self.Drag
    def get_lift(self,a):
        self.Lift = 0.5 * env.air_density * self.V**2 * veh.Sref * self.get_CL(a)
        return self.Lift
    def get_thrust_a(self,a):
        self.Thrust = self.Drag * np.cos(a) + self.weight * np.sin(self.theta) - self.Lift * np.sin(a)
        self.Thrust = self.Thrust * self.Thrust_mod
        return self.Thrust
    def get_thrust(self,a):
        self.Thrust = self.Thrust * self.Thrust_mod
        return self.Thrust
    def get_moment(self,a):
        self.Moment = 0.5 * (env.air_density*veh.Sref*veh.cbar*self.get_CM(a)*self.V**2)
    def find_alpha(self,alpha_rad):
        return (0.5 * env.air_density * self.V**2 * veh.Sref) * (self.get_CL_alpha(alpha_rad) * np.cos(alpha_rad) + self.get_CD_alpha(alpha_rad) * np.sin(alpha_rad)) - self.weight * np.cos(self.set_theta(alpha_rad))
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
        self.get_thrust_a(a)
        self.get_moment(a)
        self.get_ub(a)
        self.get_wb(a)
    def get_forces_loop(self,a):
        self.get_drag(a)
        self.get_lift(a)
        self.get_thrust(a)
        self.get_moment(a)
    def set_initials(self):
        self.get_alpha()
        self.trim(self.alpha)
        self.delta_el = math.radians(self.delta_el)
        self.set_theta(self.alpha)
        self.get_forces(self.alpha)
    def get_ub_dt(self,a): #alpha in rads and self.theta must be in rads too 
        self.ub_dt = (self.Lift/self.mass)*math.sin(a)-(self.Drag/self.mass)*math.cos(a) - (self.q)*(self.wb) - env.gravity*math.sin(self.theta) + (self.Thrust/self.mass)
        return self.ub_dt
    def get_wb_dt(self,a): #alpha in rads and self.theta must be in rads too 
        self.wb_dt = -(self.Lift/self.mass)*math.cos(a)-(self.Drag/self.mass)*math.sin(a) + (self.q)*(self.ub) + env.gravity*math.cos(self.theta)
        return self.wb_dt
    def update_V(self):
        self.V = math.sqrt(self.ub**2 + self.wb**2)
        return self.V
    def get_q_dt(self):
        self.q_dot = self.Moment / veh.inertia_yy
        return self.q_dot
    def get_theta_dt(self):
        self.theta_dt = self.q
        return self.theta_dt
    def update_alpha(self): #for in the loop calcs of alpha based on velocities
        self.alpha = math.atan(self.wb/self.ub)
        return self.alpha
    def get_dz_dt(self):
        self.dz_dt= -self.ub*math.sin(self.theta) + self.wb*math.cos(self.theta)
        return self.dz_dt
    def get_dx_dt(self):
        self.dx_dt = self.ub* math.cos(self.theta) + self.wb*math.sin(self.theta)
        return self.dx_dt
    def update_gamma(self,a):
        self.gamma = self.theta - self.alpha
        return self.gamma
    def get_derivatives(self): #alpha in rads
        self.V = self.update_V()
        self.get_forces_loop(self.alpha)
        self.get_ub_dt(self.alpha)
        self.get_wb_dt(self.alpha)
        self.get_q_dt()
        self.get_theta_dt()
        self.get_dz_dt()
        self.get_dx_dt()
    def update_state(self):
        self.ub += self.ub_dt * self.time_step
        self.wb += self.wb_dt  * self.time_step        
        self.q += self.q_dot * self.time_step
        self.theta += self.theta_dt * self.time_step
        self.alpha = self.update_alpha()
        self.gamma = self.update_gamma(self.alpha)
        self.z_e += self.dz_dt * self.time_step
        self.x_e += self.dx_dt * self.time_step
    def fetch_state(self):
        return self.Thrust,self.alpha,self.V,self.ub,self.wb,self.q,self.theta,self.z_e,self.x_e,self.delta_el * self.del_mod,self.gamma
