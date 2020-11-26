# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 17:40:03 2020

@author: A C E R
"""

"""
This code was not directly used in the final implementation but the algorithms and methodology were relied on
 heavily, shoutout to Freddie and Wan for their work on these files 
"""
import math
import numpy as np
from scipy import optimize
import env as env
import vehicle as veh
import Antonio_Coefficients_complete as coeff
import matplotlib.pyplot as plt 


# Equilibrium Conditions
q = 0
M = 0
CM = 0

# The range value of gamma
gamma = np.linspace(0,0.1,100)


W = veh.acMass * env.gravity

#the equation to find alpha, g is the list value of gamma 
def delta(alpha_x): 
        return -(coeff.CM_0 + coeff.CM_alpha*np.degrees(alpha_x))/coeff.CM_delta

def CL(alpha_x):
        
        return coeff.CL_0 + coeff.CL_alpha*np.degrees(alpha_x) + coeff.CL_delta*delta(alpha_x)
    

def CD(alpha_x):
        
        return coeff.CD_0 + coeff.CD_k*CL(alpha_x)**2

def theta(alpha_x, g):
    
        return alpha_x + g

#when the value of v = 75
V_1 = 75
#uses to put list of alpha,delta and thrust value that being produced due to the v=range value of velocity
list_alpha_1 = []
list_delta_1 = []
list_thrust_1 = []

def find_alpha(v):
      find_alpha = lambda alpha_rad : (0.5 * env.air_density * V_1**2 * veh.Sref) * (CL(alpha_rad) * np.cos(alpha_rad) + CD(alpha_rad) * np.sin(alpha_rad)) - W * np.cos(theta(alpha_rad,g))
      return find_alpha
  
#for loop in findind different value of alpha,delta and thrust with different value of gamma.
for g in gamma:
    
   
    alpha_1 = optimize.fsolve(find_alpha(V_1),0)
    
    theta(alpha_1, g)
    list_alpha_1.append(alpha_1)
    
    delta_rad_1 = delta(alpha_1)*(math.pi/180)
    list_delta_1.append(delta_rad_1)
        
    Drag = 0.5 * env.air_density * V_1**2 * veh.Sref * CD(alpha_1)
    Lift = 0.5 * env.air_density * V_1**2 * veh.Sref * CL(alpha_1)   
        
    Thrust_1 = Drag * np.cos(alpha_1) + W * np.sin(theta(alpha_1,g)) - Lift * np.sin(alpha_1) 
    list_thrust_1.append(Thrust_1)
    
    Ub = V_1*np.cos(alpha_1);
    Wb = V_1*np.sin(alpha_1);

#when the value of v is 100
V_2 = 100
#uses to put list of alpha,delta and thrust value that being produced due to the v=range value of velocity
list_alpha_2 = []
list_delta_2 = []
list_thrust_2 = []

def find_alpha(v):
      find_alpha = lambda alpha_rad : (0.5 * env.air_density * V_2**2 * veh.Sref) * (CL(alpha_rad) * np.cos(alpha_rad) + CD(alpha_rad) * np.sin(alpha_rad)) - W * np.cos(theta(alpha_rad,g))
      return find_alpha
  
#for loop in findind different value of alpha,delta and thrust with different value of gamma.
for g in gamma:
    
   
    alpha_2 = optimize.fsolve(find_alpha(V_2),0)
    
    theta(alpha_2, g)
    list_alpha_2.append(alpha_2)
    
    delta_rad_2 = delta(alpha_2)*(math.pi/180)
    list_delta_2.append(delta_rad_2)
        
    Drag = 0.5 * env.air_density * V_2**2 * veh.Sref * CD(alpha_2)
    Lift = 0.5 * env.air_density * V_2**2 * veh.Sref * CL(alpha_2)   
        
    Thrust_2 = Drag * np.cos(alpha_2) + W * np.sin(theta(alpha_2,g)) - Lift * np.sin(alpha_2) 
    list_thrust_2.append(Thrust_2)
    
    Ub = V_2*np.cos(alpha_2);
    Wb = V_2*np.sin(alpha_2);

#when the value of v = 125
V_3 = 125
#uses to put list of alpha,delta and thrust value that being produced due to the v=range value of velocity
list_alpha_3 = []
list_delta_3 = []
list_thrust_3 = []

def find_alpha(v):
      find_alpha = lambda alpha_rad : (0.5 * env.air_density * V_3**2 * veh.Sref) * (CL(alpha_rad) * np.cos(alpha_rad) + CD(alpha_rad) * np.sin(alpha_rad)) - W * np.cos(theta(alpha_rad,g))
      return find_alpha
  
#for loop in findind different value of alpha,delta and thrust with different value of gamma.
for g in gamma:
    
   
    alpha_3 = optimize.fsolve(find_alpha(V_3),0)
    
    theta(alpha_3, g)
    list_alpha_3.append(alpha_3)
    
    delta_rad_3 = delta(alpha_3)*(math.pi/180)
    list_delta_3.append(delta_rad_3)
        
    Drag = 0.5 * env.air_density * V_3**2 * veh.Sref * CD(alpha_3)
    Lift = 0.5 * env.air_density * V_3**2 * veh.Sref * CL(alpha_3)   
        
    Thrust_3 = Drag * np.cos(alpha_3) + W * np.sin(theta(alpha_3,g)) - Lift * np.sin(alpha_3) 
    list_thrust_3.append(Thrust_3)
    
    Ub = V_3*np.cos(alpha_3);
    Wb = V_3*np.sin(alpha_3);

#when the value of v is 150
V_4 = 150
#uses to put list of alpha,delta and thrust value that being produced due to the v=range value of velocity
list_alpha_4 = []
list_delta_4 = []
list_thrust_4 = []

def find_alpha(v):
      find_alpha = lambda alpha_rad : (0.5 * env.air_density * V_4**2 * veh.Sref) * (CL(alpha_rad) * np.cos(alpha_rad) + CD(alpha_rad) * np.sin(alpha_rad)) - W * np.cos(theta(alpha_rad,g))
      return find_alpha
  
#for loop in findind different value of alpha,delta and thrust with different value of gamma.
for g in gamma:
    
   
    alpha_4 = optimize.fsolve(find_alpha(V_4),0)
    
    theta(alpha_4, g)
    list_alpha_4.append(alpha_4)
    
    delta_rad_4 = delta(alpha_4)*(math.pi/180)
    list_delta_4.append(delta_rad_4)
        
    Drag = 0.5 * env.air_density * V_4**2 * veh.Sref * CD(alpha_4)
    Lift = 0.5 * env.air_density * V_4**2 * veh.Sref * CL(alpha_4)   
        
    Thrust_4 = Drag * np.cos(alpha_4) + W * np.sin(theta(alpha_4,g)) - Lift * np.sin(alpha_4) 
    list_thrust_4.append(Thrust_4)
    
    Ub = V_4*np.cos(alpha_4);
    Wb = V_4*np.sin(alpha_4);    

#plotting the graph of the thrust and delta_e against gamma    
plt.subplot(2,1,1)
plt.plot(gamma, list_thrust_1, 'b-',gamma,list_thrust_2, 'r-',gamma, list_thrust_3, 'g-',gamma,list_thrust_4, 'y-',)
plt.xlabel('Gamma rad')
plt.ylabel('Thrust N')

plt.subplot(2,1,2)
plt.plot(gamma, list_delta_1, 'b-',gamma,list_delta_2, 'r-',gamma, list_delta_3, 'g-',gamma,list_delta_4, 'y-',)
plt.xlabel('Gamma rad')
plt.ylabel('Delta e')    


   
    








