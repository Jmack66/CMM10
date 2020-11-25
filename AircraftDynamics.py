import numpy as np 
import math
import vehicle as veh 
import env
from scipy import optimize
from scipy.optimize import fsolve
import CoeffecientData as cd
#Aircraft Dynamics Class 
#temporary globals just to get function to run 
coeff, covar = cd.set_coeffecients()
class Plane():
	def __init__(self,time_step):
		self.x_e = 0
		self.z_e = -1000
		self.gamma = 0
		self.weight = veh.acMass * env.gravity
		self.m = veh.acMass
		self.CM_0 = 0
		self.time_step = time_step
		self.ub_ret = np.array([0])
		self.wb_ret = np.array([0])
		self.q_ret = np.array([0])
		self.alpha_ret = np.array([0])
		self.theta_ret = np.array([0])
		self.gamma_ret = np.array([0])
		self.ze_ret = np.array([0])
		self.del_mod = 1
	def elevator_control(self,input):
		return 0
	def get_state_vector(self):
		return 0
	def delta_0(self,alpha_x): 
		return -(coeff.get("CM_0") + coeff.get("CM_alpha")*alpha_x) / coeff.get("CM_delta")
	def CL_0(self,alpha_x):
		return coeff.get("CL_0") + coeff.get("CL_alpha")*alpha_x + coeff.get("CL_delta")*self.delta_0(alpha_x)
	def CD_0(self,alpha_x):
		return coeff.get("CD_0") + coeff.get("CD_K")*self.CL_0(alpha_x)**2
	def theta_0(self, alpha_x):
		return alpha_x + self.gamma
	def get_alpha(self,alpha_rad):
		#this is only for initial stuff will need to be done with integration in the loop
		return (0.5 * env.air_density * self.V**2 * veh.Sref) * (self.CL_0(alpha_rad) * np.cos(alpha_rad) + self.CD_0(alpha_rad) * np.sin(alpha_rad)) - self.weight * np.cos(self.theta_0(alpha_rad))
	def alpha_0(self):
		self.alpha = optimize.fsolve(self.get_alpha,0)
		return self.alpha
	def set_initials(self):
		self.alpha = self.alpha_0()
		self.delta = self.delta_0(self.alpha)
		self.Drag,self.Lift,self.Thrust,self.Moment = self.forces_idk(self.alpha)
		self.ub = self.V*np.cos(self.alpha)
		self.wb = self.V*np.sin(self.alpha)
		self.theta = self.gamma + self.alpha
		self.q = 0
		self.ub_ret[0] = self.ub
		self.wb_ret[0] = self.wb
		self.q_ret[0] = 0
		self.alpha_ret[0] = self.alpha
		self.gamma_ret[0] = self.gamma
		self.theta_ret[0] = self.alpha + self.gamma
		return self.Drag,self.Lift,self.Thrust,self.Moment,self.ub,self.wb

	def forces_idk(self, alpha):
		self.Drag = 0.5 * env.air_density * self.V**2 * veh.Sref * self.CD_0(alpha)
		self.Lift = 0.5 * env.air_density * self.V**2 * veh.Sref * self.CL_0(alpha)
		self.Thrust = self.Drag * np.cos(alpha) + self.weight * np.sin(self.theta_0(alpha)) - self.Lift * np.sin(alpha)
		self.Moment = (env.air_density*veh.Sref*veh.cbar*self.CM_0*self.V**2)/2
		return self.Drag, self.Lift, self.Thrust,self.Moment
	def get_current_coeffecients(self):
		CL = coeff.get("CL_0")+(coeff.get("CL_alpha")*self.alpha)+(coeff.get("CL_delta")*((self.del_mod)*self.delta))
		CM = coeff.get("CM_0")+(coeff.get("CM_alpha")*self.alpha)+(coeff.get("CM_delta")*((self.del_mod)*self.delta))
		CD = coeff.get("CD_0") +(coeff.get("CD_K")*CL**2)
		return CD,CL,CM
	def forces_idk_new(self,alpha):
		self.CL_new,self.CM_new,self.CD_new = self.get_current_coeffecients()
		self.Drag = 0.5 * env.air_density * self.V**2 * veh.Sref * self.CD_new
		self.Lift = 0.5 * env.air_density * self.V**2 * veh.Sref * self.CL_new
		self.Thrust = self.Drag * np.cos(alpha) + self.weight * np.sin(self.theta) - self.Lift * np.sin(alpha)
		self.Moment = (env.air_density*veh.Sref*veh.cbar*self.CM_new*self.V**2)/2
	def ubwb_dt(self,alpha_s):
		self.ub_dt = (self.Lift/self.m)*math.sin(alpha_s)-(self.Drag/self.m)*math.cos(alpha_s) - (self.q)*(self.wb) - (self.weight/self.m)*math.sin(alpha_s) + (self.Thrust/self.m)
		self.wb_dt = -(self.Lift/self.m)*math.cos(alpha_s)-(self.Drag/self.m)*math.sin(alpha_s) + (self.q)*(self.ub) + (self.weight/self.m)*math.cos(alpha_s)
		return self.ub_dt, self.wb_dt
	def dynamic_derivatives(self):
		self.forces_idk_new(self.alpha)
		self.ubwb_dt(self.alpha)
		self.V = math.sqrt(self.ub**2 + self.wb**2)
		self.q_dot = self.Moment / veh.inertia_yy
		self.theta_dot = self.q
		self.alpha_dot = math.atan(self.wb/self.ub)
		self.gamma_dot = 0 
		self.dzEz = -self.ub*math.sin(self.theta) + self.wb*math.cos(self.theta)
		print(self.alpha_dot,self.gamma_dot,self.dzEz,self.q_dot,self.ub_dt,self.wb_dt)
	def update(self):
		#assert np.rad2deg(self.alpha) + np.rad2deg(self.gamma) is np.rad2deg(self.theta), "theta is not alpha,gamma"
		self.gamma = self.theta - self.alpha
		self.alpha += self.alpha_dot * self.time_step
		self.theta = self.theta_dot * self.time_step
		if abs(np.rad2deg(self.theta)) > 360:
			print("ASDFASDFASDFASDFASDF")
			self.theta = 0
		self.z_e += (self.dzEz * self.time_step)
		self.q += (self.q_dot * self.time_step)
		self.ub += (self.ub_dt * self.time_step)
		self.wb += (self.wb_dt * self.time_step)
		#print(np.rad2deg(self.alpha),np.rad2deg(self.gamma),np.rad2deg(self.theta),self.z_e,self.q,self.ub,self.wb)
		self.store_vars()
	def store_vars(self):
		self.alpha_ret = np.append(self.alpha_ret, np.rad2deg(self.alpha))
		self.gamma_ret = np.append(self.gamma_ret, np.rad2deg(self.gamma))
		self.theta_ret = np.append(self.theta_ret, np.rad2deg(self.theta))
		self.ub_ret = np.append(self.ub_ret, self.ub)
		self.wb_ret = np.append(self.wb_ret, self.wb)
		self.q_ret = np.append(self.q_ret,np.rad2deg((self.q)))
		self.ze_ret = np.append(self.ze_ret, self.z_e)