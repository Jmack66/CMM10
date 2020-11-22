import numpy as np 
import math
import vehicle as veh 
import env
from scipy import optimize
from scipy.optimize import fsolve
import CoeffecientData as cd
import find_alpha as fa
#Aircraft Dynamics Class 
#temporary globals just to get function to run 
coeff, covar = cd.set_coeffecients()
alpha = 0
# Equilibrium Conditions
q = 0
M = 0
CM = 0

gamma_rad = 0.05
V = 100

class Plane():
	def __init__(self,time_step):
		self.ub = 0
		self.wb = 0
		self.q = 0
		self.gamma_0 = 0
		self.gamma = 0
		self.x_e = 0
		self.z_e = 0
		self.alpha = 0 
		self.weight = veh.acMass * env.gravity
		self.m = veh.acMass
		self.V = 0
		self.theta = 0
		self.time_step = 0
		self.CD = 0
		self.CL = 0
		self.D_0 = 0
		self.L_0 = 0
		self.T_0 = 0
		self.M_0 = 0
		self.D = 0
		self.L = 0
		self.T = 0
		self.M = 0
		self.CM_0 = 0
		self.ub_ret = np.array([0])
		self.wb_ret = np.array([0])
		self.q_ret = np.array([0])
		self.alpha_ret = np.array([0])
		self.theta_ret = np.array([0])
		self.gamma_ret = np.array([0])
		self.ze_ret = np.array([0])
		#dictionary allows for variables to be extracted specifically from the state vector using their name and or allows full return of the state vector
		self.state_vector = {"Ub" : self.ub, "Wb" : self.wb, "theta" : self.theta, "theta_dot" : self.q,
		 "X_earth" : self.x_e, "Z_e" : self.z_e, "Altitude" : -self.z_e, "Velocity" : self.V}
	def elevator_control(self,input):
		#input will likely be elevator angle or trim and system response will go here
		return self.state_vector.values()
	def get_state_vector(self):
		return self.state_vector
	def delta_0(self,alpha_x): 
		return -(coeff.get("CM_0") + coeff.get("CM_alpha")*np.degrees(alpha_x)) / coeff.get("CM_delta")
	def CL_0(self,alpha_x):
		return coeff.get("CL_0") + coeff.get("CL_alpha")*np.degrees(alpha_x) + coeff.get("CL_delta")*self.delta_0(alpha_x)
	def CD_0(self,alpha_x):
		return coeff.get("CD_0") + coeff.get("CD_K")*self.CL_0(alpha_x)**2
	def theta_0(self, alpha_x):
		return alpha_x + gamma_rad
	def get_alpha(self,alpha_rad):
		#this is only for initial stuff will need to be done with integration in the loop
		return (0.5 * env.air_density * self.V**2 * veh.Sref) * (self.CL_0(alpha_rad) * np.cos(alpha_rad) + self.CD_0(alpha_rad) * np.sin(alpha_rad)) - self.weight * np.cos(self.theta_0(alpha_rad))
	def alpha_0(self):
		self.alpha = optimize.fsolve(self.get_alpha,0)
		return alpha
	def set_initials(self):
		pass_0 = self.alpha_0()
		self.D_0,self.L_0,self.T_0,self.M_0 = self.forces_idk(pass_0)
		self.ub = self.V*np.cos(pass_0)
		self.wb = self.V*np.sin(pass_0)
		self.ub_ret[0] = self.ub
		self.wb_ret[0] = self.wb
		self.q_ret[0] = 0
		self.alpha_ret[0] = pass_0
		self.gamma_ret[0] = self.gamma_0
		self.theta_ret[0] = self.alpha_ret[0] + self.gamma_ret[0]
		return self.D_0,self.L_0,self.T_0,self.M_0,self.ub,self.wb

	def forces_idk(self, alpha):
		self.Drag = 0.5 * env.air_density * self.V**2 * veh.Sref * self.CD_0(alpha)
		self.Lift = 0.5 * env.air_density * self.V**2 * veh.Sref * self.CL_0(alpha)
		self.Thrust = self.Drag * np.cos(alpha) + self.weight * np.sin(self.theta_0(alpha)) - self.Lift * np.sin(alpha)
		self.Moment = (env.air_density*veh.Sref*veh.cbar*self.CM_0*self.V**2)/2
		return self.Drag, self.Lift, self.Thrust,self.Moment
	def forces_idk_new(self,alpha):
		self.CL_new,self.CM_new,self.CD_new = fa.get_current_coeffecients(self.alpha)
		self.Drag = 0.5 * env.air_density * self.V**2 * veh.Sref * self.CD_new
		self.Lift = 0.5 * env.air_density * self.V**2 * veh.Sref * self.CL_new
		self.Thrust = self.Drag * np.cos(alpha) + self.weight * np.sin(self.theta) - self.Lift * np.sin(alpha)
		self.Moment = (env.air_density*veh.Sref*veh.cbar*self.CM_new*self.V**2)/2
	def ubwb_dt(self,alpha_s):
		self.ub_dt = (self.Lift/self.m)*math.sin(alpha_s)-(self.D/self.m)*math.cos(alpha_s) - (self.q)*(self.wb) -(self.weight/self.m)*math.sin(alpha_s)+ (self.Thrust/self.m)
		self.wb_dt = -(self.Lift/self.m)*math.cos(alpha_s)-(self.D/self.m)* math.sin(alpha_s) + (self.q)*(self.ub) +(self.weight/self.m)*math.cos(alpha_s)
		return self.ub_dt, self.wb_dt
	def dynamic_derivatives(self):
		self.forces_idk_new(self.alpha)
		self.ubwb_dt(self.alpha)
		self.V = math.sqrt(self.ub**2 + self.wb**2)
		self.q_dot = self.Moment / veh.inertia_yy
		self.theta_dot = self.q
		print(self.theta_dot)
		self.alpha_dot = math.atan(self.wb/self.ub)
		self.gamma_dot = self.theta - self.alpha_dot
		self.dzEz = -self.ub*math.sin(self.theta) + self.wb*math.cos(self.theta)
	def update(self):
		self.alpha += (self.alpha_dot)
		self.gamma += (self.gamma_dot)
		self.theta = self.alpha + self.gamma
		self.z_e += (self.dzEz * self.time_step)
		self.q += (self.q_dot * self.time_step)
		self.ub += (self.ub_dt * self.time_step)
		self.wb += (self.wb_dt * self.time_step)
		self.store_vars()
	def store_vars(self):
		self.alpha_ret = np.append(self.alpha_ret, self.alpha)
		self.gamma_ret = np.append(self.gamma_ret, self.gamma)
		self.theta_ret = np.append(self.theta_ret, self.theta)
		self.ub_ret = np.append(self.ub_ret, self.ub)
		self.wb_ret = np.append(self.wb_ret, self.wb)
		self.q_ret = np.append(self.q_ret, self.q)
		self.ze_ret = np.append(self.q_ret, self.z_e)
