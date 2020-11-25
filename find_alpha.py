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

import matplotlib.pyplot as plt

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
        return -(coeff.get("CM_0") + coeff.get("CM_alpha")*alpha_x/coeff.get("CM_delta"))

def CL(alpha_x):
        return coeff.get("CL_0") + coeff.get("CL_alpha")*alpha_x + coeff.get("CL_delta")*delta(alpha_x)
    

def CD(alpha_x):
        return coeff.get("CD_0") + coeff.get("CD_K")*CL(alpha_x)**2

def theta(alpha_x):
        return alpha_x + gamma_rad
W = veh.acMass * env.gravity
find_alpha = lambda alpha_rad: (0.5 * env.air_density * V**2 * veh.Sref) * (CL(alpha_rad) * np.cos(alpha_rad) + CD(alpha_rad) * np.sin(alpha_rad)) - W * np.cos(theta(alpha_rad))

alpha = optimize.fsolve(find_alpha,0)
print(alpha)
delta_rad = delta(alpha)*(math.pi/180)
CL_2 = coeff.get("CL_0")+(coeff.get("CL_alpha")*alpha)+coeff.get("CL_delta")*((delta_rad))
CD_2 = coeff.get("CD_0") +(coeff.get("CD_K")*CL_2**2)

cd = CD(alpha)
cl = CL(alpha)

print((cl,CL_2),(cd,CD_2))

    


theta_ = alpha + gamma_rad

# print('\nAngle of Attack = ' , float(np.round(alpha, 5)), 'rad')
# print('theta =' , float(np.round(theta_, 5)), 'rad')
# print('delta e = ', float(np.round(delta_rad, 5)), 'rad')



Drag = 0.5 * env.air_density * V**2 * veh.Sref * CD(alpha)
Lift = 0.5 * env.air_density * V**2 * veh.Sref * CL(alpha)   

Thrust = Drag * np.cos(alpha) + W * np.sin(theta(alpha)) - Lift * np.sin(alpha) 

Ub = V*np.cos(alpha)
Wb = V*np.sin(alpha)

def get_current_coeffecients(alpha,del_mod):
        CL=coeff.get("CL_0")+(coeff.get("CL_alpha")*alpha)+(coeff.get("CL_delta")*((del_mod)*delta_rad))
        CM=coeff.get("CM_0")+(coeff.get("CM_alpha")*alpha)+(coeff.get("CM_delta")*((del_mod)*delta_rad))
        CD=coeff.get("CD_0") +(coeff.get("CD_K")*CL**2)
        return CL,CM,CD

# print ('Thrust = ', float(np.round(Thrust, 2)), 'N')
# print('Ub =', float(np.round(Ub, 3)), 'm/s')
# print('Wb = ', float(np.round(Wb, 4)), 'm/s')

cf_alpha = np.array([])
for a in cd.alpha:
        cf_alpha = np.append(cf_alpha,CD(a))
cf_alpha.reshape(1,10)


def getPlots():
    #NEED TO ADD CALCILATED FITS TO PLOT
    fig, (ax1,ax2,ax3) = plt.subplots(3, sharex=True)
    ax1.set(ylabel='CD_wing')
    ax1.plot(cd.alpha,cd.CD,'ro')
    ax2.set(ylabel='CL_wing')
    ax1.plot(cd.alpha,cf_alpha,'b-')
    ax2.plot(cd.alpha,cd.CL,'bo')
    ax3.set(ylabel='CM_wing')
    ax3.plot(cd.alpha,cd.CM,'go')
    plt.show()
    return fig,fig2

getPlots()