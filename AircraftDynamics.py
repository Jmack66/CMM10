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










