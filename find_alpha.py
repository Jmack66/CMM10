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
import CoeffecientData
import matplotlib.pyplot as plt
coeff, covar = CoeffecientData.set_coeffecients()
alpha = 0
# Equilibrium Conditions
q = 0
M = 0
CM = 0

# Given Values
# Potentially use input function or other for other variables.

gamma_rad = 0.05
V = 100


def delta(alpha_x): 
        return -(coeff.get("CM_0") + coeff.get("CM_alpha")*np.degrees(alpha_x)) / coeff.get("CM_delta")

def CL(alpha_x):
        
        return coeff.get("CL_0") + coeff.get("CL_alpha")*np.degrees(alpha_x) + coeff.get("CL_delta")*delta(alpha_x)
    

def CD(alpha_x):
        
        return coeff.get("CD_0") + coeff.get("CD_K")*CL(alpha_x)**2

def theta(alpha_x):
    
        return alpha_x + gamma_rad
    
        
W = veh.acMass * env.gravity
    
find_alpha = lambda alpha_rad: (0.5 * env.air_density * V**2 * veh.Sref) * (CL(alpha_rad) * np.cos(alpha_rad) + CD(alpha_rad) * np.sin(alpha_rad)) - W * np.cos(theta(alpha_rad))

time = np.linspace(0,100,100)
big_pee = np.zeros(100)
for i in time - 1:
        big_pee[int(i)] = find_alpha(i)


def solve_alpha(last_alpha):
        alpha = optimize.fsolve(find_alpha,[last_alpha,last_alpha+ 5])
        return alpha


def get_delta_rad(alpha):
        delta_rad = delta(alpha)*(math.pi/180)
        return delta_rad

def get_thrust(alpha):
        Thrust = Drag * np.cos(alpha) + W * np.sin(theta(alpha)) - Lift * np.sin(alpha) 
        return Thrust


# print('Angle of Attack = ' , float(np.round(alpha, 5)), 'rad')
# print('theta =' , float(np.round(alpha + gamma_rad, 5)), 'rad')
# print('delta e = ', float(np.round(delta_rad, 5)), 'rad')



Drag = 0.5 * env.air_density * V**2 * veh.Sref * CD(alpha)
Lift = 0.5 * env.air_density * V**2 * veh.Sref * CL(alpha)   

Thrust = Drag * np.cos(alpha) + W * np.sin(theta(alpha)) - Lift * np.sin(alpha) 
Ub = V*np.cos(alpha)
Wb = V*np.sin(alpha)

print ('Thrust = ', float(np.round(Thrust, 2)), 'N')
print('Ub =', float(np.round(Ub, 3)), 'm/s')
print('Wb = ', float(np.round(Wb, 4)), 'm/s')