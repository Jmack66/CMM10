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
tmin=0
tmax=100
#initial conditions
t0 = 0
ub_dt_at_t0=find_alpha.Ub
wb_dt_at_t0=find_alpha.Wb
#t_final is the solution interval specification
t_final=100
step_size=0.1
n_step= math.ceil(t_final/step_size)


#Define Solution Storage Arrays
ub_dt_Eul =np.zeros(100)
wb_dt_Eul=np.zeros(100)
t_Eul = np.linspace(0,1000,1)

#begin arrays with the initial conditions
ub_dt_Eul[0]=ub_dt_at_t0
wb_dt_Eul[0]=wb_dt_at_t0
t_Eul[0]=t0

#Populating the t array values
# for i in range(n_step - 1):
#     t_Eul[i+1]=t_Eul[i] + step_size

print(t_Eul)


q_0= find_alpha.q
def q_dt(t,q):
    dq_dt = (aero_coefficients.CM)/(vehicle.inertia_yy)
    return dq_dt
q_t=scipy.integrate.solve_ivp(q_dt,(0,100),([q_0]),dense_output=True)




#p = q_t.q_t(real_t)
# t = np.linspace(0, 15, 300)
# z = sol.sol(t)
#print(p.T)

y = np.array([])
y = q_t.y
print(y)
print(q_t.t)
#y.reshape(1,8)

L=0.5*(env.air_density)*(find_alpha.V**2)*(vehicle.Sref)*(aero_coefficients.CL)
D=0.5*(env.air_density)*(find_alpha.V**2)*(vehicle.Sref)*(aero_coefficients.CD)
M=0.5*(env.air_density)*(find_alpha.V**2)*(vehicle.Sref)*(vehicle.cbar)*(aero_coefficients.CM)
T=find_alpha.Thrust
W=find_alpha.W

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  
"""If flight path angle (gamma) is constant, then as alpha=theta-gamma and
theta= q*t +theta_0 """
#alpha=alpha_0 for first iteration
#alpha=theta-gamma=(q*t - alpha)-gamma  for all further iterations
#alpha=theta-gamma=(q*t + alpha)-gamma  for all further iterations???????

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#check with finlay that okay: y is a discrete array with 8 values so the time value passed into it needs to be an int this was part of the usse
#then also the q_t is a class and the y values from it need to be extracted as done aboce with y
alpha_f = np.zeros(100)
def ubwb_dt(t,ub,wb):
    alpha_s = find_alpha.solve_alpha(alpha_f[int(t) - 1])
    print(alpha_s[0])
    alpha_f[int(t)] = alpha_s[0]
    ub_dt= (L/M)*math.sin(alpha_s)-(D/M)*math.cos(alpha_s)\
        -(y[int(t)])*(int(wb)) -(W/M)*math.sin(alpha_s)+ (T/M)
    wb_dt = -(L/M)*math.cos(alpha_s)-(D/M)* math.sin(alpha_s)\
        +(y[int(t)])*(int(ub)) +(W/M)*math.cos(alpha_s)
    print(type(wb_dt))
    print(type(ub_dt))  
    return ub_dt , wb_dt
#NOTE: I think that the find_alpha.find_alpha function cannot be used here
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#And finally, here we use the Euler method on our functions 
slope_ub_dt = np.zeros(100)
slope_wb_dt = np.zeros(100)
for i in range(100):
    #this bit seems to be the resolution of the solution
    slope_ub_dt[i],slope_wb_dt[i] = ubwb_dt(t_Eul[i],ub_dt_Eul[i],wb_dt_Eul[i])
    ub_dt_Eul[i + 1] = ub_dt_Eul[i] + step_size*(slope_ub_dt[i])
    wb_dt_Eul[i+1] = wb_dt_Eul[i] +step_size*(slope_wb_dt[i])
plt.plot(wb_dt_Eul,t_Eul,'r--')
plt.show()








