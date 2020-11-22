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
import CoeffecientData as cd


coeff, covar = cd.set_coeffecients()
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
        return -(coeff.get("CM_0") + coeff.get("CM_alpha")*np.degrees(alpha_x))/coeff.get("CM_delta")

def CL(alpha_x):
        
        return coeff.get("CL_0") + coeff.get("CL_alpha")*np.degrees(alpha_x) + coeff.get("CL_delta")*delta(alpha_x)
    

def CD(alpha_x):
        
        return coeff.get("CD_0") + coeff.get("CD_K")*CL(alpha_x)**2

def theta(alpha_x):
    
        return alpha_x + gamma_rad
    
        
W = veh.acMass * env.gravity
    
find_alpha = lambda alpha_rad: (0.5 * env.air_density * V**2 * veh.Sref) * (CL(alpha_rad) * np.cos(alpha_rad) + CD(alpha_rad) * np.sin(alpha_rad)) - W * np.cos(theta(alpha_rad))

alpha = optimize.fsolve(find_alpha,0)
delta_rad = delta(alpha)*(math.pi/180)
theta_ = alpha + gamma_rad

print('\nAngle of Attack = ' , float(np.round(alpha, 5)), 'rad')
print('theta =' , float(np.round(theta_, 5)), 'rad')
print('delta e = ', float(np.round(delta_rad, 5)), 'rad')



Drag = 0.5 * env.air_density * V**2 * veh.Sref * CD(alpha)
Lift = 0.5 * env.air_density * V**2 * veh.Sref * CL(alpha)   

Thrust = Drag * np.cos(alpha) + W * np.sin(theta(alpha)) - Lift * np.sin(alpha) 

Ub = V*np.cos(alpha)
Wb = V*np.sin(alpha)

def get_current_coeffecients(alpha):
    CL=coeff.get("CL_0")+(coeff.get("CL_alpha")*alpha)+(coeff.get("CL_delta")*delta(alpha))
    CM=coeff.get("CM_0")+(coeff.get("CM_alpha")*alpha)+(coeff.get("CM_delta")*delta(alpha))
    CD=coeff.get("CD_0") +(coeff.get("CD_K")*CL**2)
    return CL,CM,CD

print ('Thrust = ', float(np.round(Thrust, 2)), 'N')
print('Ub =', float(np.round(Ub, 3)), 'm/s')
print('Wb = ', float(np.round(Wb, 4)), 'm/s')


