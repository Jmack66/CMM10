# importing modules
import numpy as np
import math
from scipy import optimize
delim= "---------------------------------------"

#--------------------------------------
# importing module with aerodynamics model 
# as tables of CL CM vs alpha
#    tables of CD vs CL
# and tables of CL_el and CM_el vs delta_el 
import aero_table
#--------------------------------------
"""LIFT EQUATIONS"""
#--------------------------------------
# Lift vs alpha for wing

# Initial guesses for the fitting
# i.e., initial values of a and b
CL_0 = 0.0410
CL_alpha = 0.1

# Functional form to fit to data
def CL_a_func(x, a, b):
    return a + b * x

# Fitting (find a and b of the above function)  
# using the python module optimize from scipy.
# params contains the fitted values of a and b
# params_covariance contains a measure of the achieved 
# accuracy 
params, params_covariance = optimize.curve_fit(CL_a_func, aero_table.alpha, aero_table.CL,
        p0=[CL_0, CL_alpha])

CL_0 = params[0]
CL_alpha = params[1]
#--------------------------------------

#Lift vs delta_elevator, for the elevator
CL_delta = 0.003

def CL_d_func(x, a):
    return a * x

params, params_covariance = optimize.curve_fit(CL_d_func, aero_table.delta_el, aero_table.CL_el,
        p0=[CL_delta])

CL_delta = params[0]
#--------------------------------------
"""Drag Equations"""
#--------------------------------------
# CD vs CL
CD_0 = 0.026
CD_k = 0.045

def CD_CL_func(x, a, b):
    return a + b * x**2.0

params, params_covariance = optimize.curve_fit(CD_CL_func, aero_table.CL, aero_table.CD,
        p0=[CD_0, CD_k])

CD_0 = params[0]
CD_k = params[1]
#--------------------------------------
"""Moment Equations"""
#--------------------------------------
# Moment vs alpha
CM_0 = 0.007
CM_alpha = -0.01
def CM_alpha_func(x, a, b):
    return a + b * x

params, params_covariance = optimize.curve_fit(CM_alpha_func, aero_table.alpha, aero_table.CM,
        p0=[CM_0, CM_alpha])

CM_0 = params[0]
CM_alpha = params[1]
#--------------------------------------
#Moment vs delta_elevator
CM_delta = -0.004
def CM_d_func(x, a):
    return a * x

params, params_covariance = optimize.curve_fit(CM_d_func, aero_table.delta_el, aero_table.CM_el,
        p0=[CM_delta])

CM_delta = params[0]

# TO BE COMPLETED HERE
#--------------------------------------
"""PRINTING RESULTS FOR INSPECTION"""
print(delim)
print("CL0, CL_alpha andCL_delta respectively")
print(CL_0,"|", CL_alpha,"|", CL_delta)
print(delim)
print("CD0 and K respectively")
print(CD_0,"|",CD_k)
print(delim)
print("CM0, CM_alpha and CM_delta respectively")
print(CM_0,"|", CM_alpha,"|", CM_delta)
#--------------------------------------


