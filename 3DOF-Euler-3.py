import scipy as scipy
import aero_coefficients
from scipy import integrate
import find_alpha 
import vehicle
import env
import math as math
import numpy as np
import matplotlib.pyplot as plt
#lecture 9, stiff equations was a real help
"""The only new things added on 20/11/2020 was reference to CM,
CL and CD; these are given in an adapted form of the 
Antonio_Coefficients_Complete file, now named aero_coefficients"""

def euler_method(F,x0,y0,h,x):
    y = 0
    ys = np.array([])
    while x0 < x:
        y = y + h * F(y, x0)
        ys = np.append(ys,y)
        x0 = x0 + h
    return ys

def q_dt(t,q):
    dq_dt = (aero_coefficients.CM)/(vehicle.inertia_yy)
    return dq_dt

ys = euler_method(q_dt,0,0,0.1,100)

print(ys)
#t_final is the solution interval specification
t_final=100
step_size=0.1

n_step= math.ceil(t_final/step_size)


#Define Solution Storage Arrays
ub_dt_Eul =np.zeros(n_step+1)
wb_dt_Eul=np.zeros(n_step+1)
q_dt_Eul=np.zeros(n_step+1)
t_Eul=np.zeros(n_step+1)

q_dt_Eul[0] = 0


#begin arrays with the initial conditions
ub_dt_Eul[0]=0
wb_dt_Eul[0]=0
t_Eul[0]=0

#Populating the t array values
for i in range(n_step):
    t_Eul[i+1]=t_Eul[i] + step_size
    
q_0= find_alpha.q

q_t=scipy.integrate.solve_ivp(q_dt,(t_Eul),[q_0])



L=0.5*(env.air_density)*(find_alpha.V**2)*(vehicle.Sref)*(aero_coefficients.CL)
D=0.5*(env.air_density)*(find_alpha.V**2)*(vehicle.Sref)*(aero_coefficients.CD)
M=0.5*(env.air_density)*(find_alpha.V**2)*(vehicle.Sref)*(vehicle.cbar)*(aero_coefficients.CM)
T=find_alpha.Thrust
W=find_alpha.W






#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#If flight path angle (gamma) is constant, then as alpha=theta-gamma and
#theta= q*t +theta_0 
#alpha=alpha_0 for first iteration
#alpha=theta-gamma=(q*t +alpha)-gamma  for all further iterations

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#check with finlay that okay: y is a discrete array with 8 values so the time value passed into it needs to be an int this was part of the usse
#then also the q_t is a class and the y values from it need to be extracted as done aboce with y
def ubwb_dt(t,ub,wb):
    ub_dt= (L/M)*math.sin(find_alpha.find_alpha(t))-(D/M)*math.cos(find_alpha.find_alpha(t))\
        -(ys[int(t)])*(int(wb)) -(W/M)*math.sin(find_alpha.find_alpha(t))+ (T/M)
    wb_dt = -(L/M)*math.cos(find_alpha.find_alpha(t))-(D/M)* math.sin(find_alpha.find_alpha(t))\
        +(ys[int(t)])*(int(ub)) +(W/M)*math.cos(find_alpha.find_alpha(t))
    return ub_dt , wb_dt




#NOTE: I think that the find_alpha.find_alpha function cannot be used here


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#And finally, here we use the Euler method on our functions
slope_ub_dt = np.zeros(n_step+1)
slope_wb_dt = np.zeros(n_step+1)
for i in range(0,8):
    #this bit seems to be the resolution of the solution
    slope_ub_dt[i],slope_wb_dt[i] = ubwb_dt(t_Eul[i],ub_dt_Eul[i],wb_dt_Eul[i])
    ub_dt_Eul[i + 1] = ub_dt_Eul[i] + step_size*(slope_ub_dt[i])
    wb_dt_Eul[i+1] = wb_dt_Eul[i] +step_size*(slope_wb_dt[i])
    print("ub_dt_Eul[i]=",ub_dt_Eul[i],"\nwb_dt_Eul[i]=", wb_dt_Eul[i])
plt.plot(wb_dt_Eul,t_Eul,'r--')
#,ub_dt_Eul,t_Eul,'g^',
plt.show()








