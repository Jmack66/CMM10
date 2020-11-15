import numpy as np 
import vehicle as veh 
import env
from scipy.optimize import fsolve
import CoeffecientData
#Aircraft Dynamics Class 
#temporary globals just to get function to run 
coeff, covar = CoeffecientData.set_coeffecients()
alpha = 0
# Equilibrium Conditions
q = 0
M = 0
CM = 0

gamma_rad = 0.05
V = 100

class Plane():
	def __init__(self):
		self.ub = 0
		self.wb = 0
		self.q = 0
		self.x_e = 0
		self.z_e = 0
		self.alpha = 0 
		self.weight = veh.acMass * env.gravity
		#dictionary allows for variables to be extracted specifically from the state vector using their name and or allows full return of the state vector
		self.state_vector = {"Ub" : self.ub, "Wb" : self.wb, "theta" : self.theta, "theta_dot" : self.q,
		 "X_earth" : self.x_e, "Z_e" : self.z_e, "Altitude" : -self.z_e}
	def elevator_control(self,input):
		#input will likely be elevator angle or trim and system response will go here
		return self.state_vector.values()
	def get_state_vector(self):
		return self.state_vector
	def delta(self,alpha_x): 
		return -(coeff.get("CM_0") + coeff.get("CM_alpha")*np.degrees(alpha_x)) / coeff.get("CM_delta")
	def CL(self,alpha_x):
		return coeff.get("CL_0") + coeff.get("CL_alpha")*np.degrees(alpha_x) + coeff.get("CL_delta")*self.delta(alpha_x)
	def CD(self,alpha_x):
		return coeff.get("CD_0") + coeff.get("CD_K")*self.CL(alpha_x)**2
	def theta(self, alpha_x):
		return alpha_x + gamma_rad
	def find_alpha(self,alpha_rad):
		return (0.5 * env.air_density * V**2 * veh.Sref) * (self.CL(alpha_rad) * np.cos(alpha_rad) + self.CD(alpha_rad) * np.sin(alpha_rad)) - self.weight * np.cos(self.theta(alpha_rad))






