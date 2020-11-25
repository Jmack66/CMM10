# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 17:40:03 2020

@author: A C E R
"""

import math
import numpy as np
from scipy import optimize
from scipy.optimize import fsolve
import env as env
import vehicle as veh
import Antonio_Coefficients_complete as coeff
import matplotlib.pyplot as plt 


# Equilibrium Conditions
q = 0
M = 0
CM = 0

# Fixed value for gamma.


#The range value of velocity from 75 to 150 with number of step = 100
V = np.linspace(75,150,100)



W = veh.acMass * env.gravity

#Equation needed to find alpha.    
def delta(alpha_x): 
        return -(coeff.CM_0 + coeff.CM_alpha*np.degrees(alpha_x))/coeff.CM_delta

def CL(alpha_x):
        
        return coeff.CL_0 + coeff.CL_alpha*np.degrees(alpha_x) + coeff.CL_delta*delta(alpha_x)
    

def CD(alpha_x):
        
        return coeff.CD_0 + coeff.CD_k*CL(alpha_x)**2
#when gamma is equal to 0.025 rad
gamma_rad_1 = 0.05

#uses to put list of alpha,delta and thrust value that being produced due to the v=range value of velocity
list_alpha_1 = []
list_delta_1 = []
list_thrust_1= []
def theta(alpha_x):
    
        return alpha_x + gamma_rad_1

def find_alpha(v):
      find_alpha = lambda alpha_rad : (0.5 * env.air_density * v**2 * veh.Sref) * (CL(alpha_rad) * np.cos(alpha_rad) + CD(alpha_rad) * np.sin(alpha_rad)) - W * np.cos(theta(alpha_rad))
      return find_alpha
#using for loop to get multiple answer for alpha,delta and thrust
#Append is used to store the value of alpha,delta and thrust inside list_alpha,list_delta and list_thrust respectively
alpha_1 = optimize.fsolve(find_alpha(100),0)
print(alpha_1)
for v in V:
    
    list_alpha_1.append(alpha_1)
    
    delta_rad_1 = delta(alpha_1)*(math.pi/180)
    list_delta_1.append(delta_rad_1)
        
    Drag = 0.5 * env.air_density * v**2 * veh.Sref * CD(alpha_1)
    Lift = 0.5 * env.air_density * v**2 * veh.Sref * CL(alpha_1)   
        
    Thrust_1 = Drag * np.cos(alpha_1) + W * np.sin(theta(alpha_1)) - Lift * np.sin(alpha_1) 
    list_thrust_1.append(Thrust_1)    
    
    Ub = V*np.cos(alpha_1);
    Wb = V*np.sin(alpha_1);
    
#for differen value of gamma
gamma_rad_2 = 0.05

#uses to put list of alpha,delta and thrust value that being produced due to the v=range value of velocity
list_alpha_2 = []
list_delta_2 = []
list_thrust_2= []
def theta(alpha_x):
    
        return alpha_x + gamma_rad_2

def find_alpha(v):
      find_alpha = lambda alpha_rad : (0.5 * env.air_density * v**2 * veh.Sref) * (CL(alpha_rad) * np.cos(alpha_rad) + CD(alpha_rad) * np.sin(alpha_rad)) - W * np.cos(theta(alpha_rad))
      return find_alpha
  
#using for loop to get multiple answer for alpha,delta and thrust
#Append is used to store the value of alpha,delta and thrust inside list_alpha,list_delta and list_thrust respectively
for v in V:
    alpha_2 = optimize.fsolve(find_alpha(v),0)
    list_alpha_2.append(alpha_2)
    
    delta_rad_2 = delta(alpha_2)*(math.pi/180)
    list_delta_2.append(delta_rad_2)
        
    Drag = 0.5 * env.air_density * v**2 * veh.Sref * CD(alpha_2)
    Lift = 0.5 * env.air_density * v**2 * veh.Sref * CL(alpha_2)   
        
    Thrust_2 = Drag * np.cos(alpha_2) + W * np.sin(theta(alpha_2)) - Lift * np.sin(alpha_2) 
    list_thrust_2.append(Thrust_2)    
    
    Ub = V*np.cos(alpha_2);
    Wb = V*np.sin(alpha_2);
    
#when gamma is equal to 0.075 rad
gamma_rad_3 = 0.075

#uses to put list of alpha,delta and thrust value that being produced due to the v=range value of velocity
list_alpha_3 = []
list_delta_3 = []
list_thrust_3= []
def theta(alpha_x):
    
        return alpha_x + gamma_rad_3

def find_alpha(v):
      find_alpha = lambda alpha_rad : (0.5 * env.air_density * v**2 * veh.Sref) * (CL(alpha_rad) * np.cos(alpha_rad) + CD(alpha_rad) * np.sin(alpha_rad)) - W * np.cos(theta(alpha_rad))
      return find_alpha
  
#using for loop to get multiple answer for alpha,delta and thrust
#Append is used to store the value of alpha,delta and thrust inside list_alpha,list_delta and list_thrust respectively
for v in V:
    alpha_3 = optimize.fsolve(find_alpha(v),0)
    list_alpha_3.append(alpha_3)
    
    delta_rad_3 = delta(alpha_3)*(math.pi/180)
    list_delta_3.append(delta_rad_3)
        
    Drag = 0.5 * env.air_density * v**2 * veh.Sref * CD(alpha_3)
    Lift = 0.5 * env.air_density * v**2 * veh.Sref * CL(alpha_3)   
        
    Thrust_3 = Drag * np.cos(alpha_3) + W * np.sin(theta(alpha_3)) - Lift * np.sin(alpha_3) 
    list_thrust_3.append(Thrust_3)    
    
    Ub = V*np.cos(alpha_3);
    Wb = V*np.sin(alpha_3);
    
#when value of gamma is 0.1
gamma_rad_4 = 0.1

#uses to put list of alpha,delta and thrust value that being produced due to the v=range value of velocity
list_alpha_4 = []
list_delta_4 = []
list_thrust_4= []
def theta(alpha_x):
    
        return alpha_x + gamma_rad_4

def find_alpha(v):
      find_alpha = lambda alpha_rad : (0.5 * env.air_density * v**2 * veh.Sref) * (CL(alpha_rad) * np.cos(alpha_rad) + CD(alpha_rad) * np.sin(alpha_rad)) - W * np.cos(theta(alpha_rad))
      return find_alpha
  
#using for loop to get multiple answer for alpha,delta and thrust
#Append is used to store the value of alpha,delta and thrust inside list_alpha,list_delta and list_thrust respectively
for v in V:
    alpha_4 = optimize.fsolve(find_alpha(v),0)
    list_alpha_4.append(alpha_4)
    
    delta_rad_4 = delta(alpha_4)*(math.pi/180)
    list_delta_4.append(delta_rad_4)
        
    Drag = 0.5 * env.air_density * v**2 * veh.Sref * CD(alpha_4)
    Lift = 0.5 * env.air_density * v**2 * veh.Sref * CL(alpha_4)   
        
    Thrust_4 = Drag * np.cos(alpha_4) + W * np.sin(theta(alpha_4)) - Lift * np.sin(alpha_4) 
    list_thrust_4.append(Thrust_4)    
    
    Ub = V*np.cos(alpha_4);
    Wb = V*np.sin(alpha_4);    
#Plotting the graph for Thrust and delta_e against velocity.    
plt.subplot(2,1,1)
plt.plot(V, list_thrust_1, 'b-',V,list_thrust_2, 'r-',V, list_thrust_3, 'g-',V,list_thrust_4, 'y-',)
plt.xlabel('Velocity m/s')
plt.ylabel('Thrust N')

plt.subplot(2,1,2)
plt.plot(V, list_delta_1, 'b-',V,list_delta_2, 'r-',V, list_delta_3, 'g-',V,list_delta_4, 'y-',)
plt.xlabel('Velocity m/s')
plt.ylabel('Delta e')    


   
    








