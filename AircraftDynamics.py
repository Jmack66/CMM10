import numpy as np 


#Aircraft Dynamics Class 

class Plane():
	def __init__(self):
		self.ub = 0
		self.wb = 0
		self.theta = 0
		self.q = 0
		self.x_e = 0
		self.z_e = 0
		#dictionary allows for variables to be extracted specifically from the state vector using their name and or allows full return of the state vector
		self.state_vector = {"Ub" : self.ub, "Wb" : self.wb, "theta" : self.theta, "theta_dot" : self.q,
		 "X_earth" : self.x_e, "Z_e" : self.z_e, "Altitude" : -self.z_e}
	def elevator_control(self,input):
		#input will likely be elevator angle or trim and system response will go here
		return self.state_vector.values()
	def get_state_vector(self):
		return self.state_vector
	def find_alpha(self,alpha):
		#not complete at all but a start of implementation to go off of
		return -0.5*env.air_density*(V**2)*veh.Sref*(CL*np.cos(alpha) + CD*np.sin(alpha)) + W*np.cos(alpha + gamma)










