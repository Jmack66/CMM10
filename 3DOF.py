"""3dof solver"""
import scipy as scipy
import scipy.integrate 
import math as math
import find_alpha 
import vehicle
import env
print(find_alpha.q)


tmin=0
tmax=100
""""tmin is the start of the interval to be examined, tmax the end"""


diff_q = (vehicle.acMass)/(vehicle.inertia_yy)
"""diff_q = M/Iyy; these values both come from vehicle.py"""
q_t=scipy.integrate.solve_ivp(diff_q,(tmin,tmax),find_alpha.q,method='RK45',t_eval=None, dense_output=False, events=None, vectorized=False, args=None)
#find_alpha.q is the initial state of q(t)


#diff_Theta=q
"""as theta is dependant on q, we must solve q first"""
#diff_X_earth= Ub*math.cos(theta) +Wb*math.cos(theta)
#diff_Z_earth= -Ub*math.sin(theta) +Wb*math.cos(theta)


#scipy.integrate.solve_ivp()
"""The above equation allows us to solve the ODE equations;"""
#diff_Wb= ((-L/M)*math.cos(alpha)) - ((D/M)*math.sin(alpha)) +q*Ub -((W/M)*math.cos(theta))
""""The function of Wb w/ respect to time, available to call with solve_IVP"""
#diff_Ub= ((L/M)*math.sin(alpha)) - ((D/M)*math.cos(alpha)) -q*Wb -((W/M)*math.sin(theta)) +(T/M)
""""Similarly, a function for Ub"""