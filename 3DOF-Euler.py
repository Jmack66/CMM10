import scipy as scipy
from scipy import integrate
import find_alpha 
import vehicle
import env
import math as math
import numpy as np
#lecture 9, stiff equations was a real help
tmin=0
tmax=100

q_0= find_alpha.q
def q_dt(t,q):
    dq_dt = (vehicle.acMass)/(vehicle.inertia_yy)
    return dq_dt
q_t=scipy.integrate.solve_ivp(q_dt,(tmin,tmax),([q_0]))

y = np.array([])
y = q_t.y
y.reshape(1,8)

L=100
D=100
T=find_alpha.Thrust
M=vehicle.acMass
W=find_alpha.W

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#check with finlay that okay: y is a discrete array with 8 values so the time value passed into it needs to be an int this was part of the usse
#then also the q_t is a class and the y values from it need to be extracted as done aboce with y
def ubwb_dt(t,ub,wb):
    ub_dt= (L/M)*math.sin(find_alpha.alpha)-(D/M)*math.cos(find_alpha.alpha)\
        -(y[int(t)])*(int(wb)) -(W/M)*math.sin(find_alpha.alpha)+ (T/M)
    wb_dt = -(L/M)*math.cos(find_alpha.alpha)-(D/M)* math.sin(find_alpha.alpha)\
        +(y[int(t)])*(int(ub)) +(W/M)*math.cos(find_alpha.alpha)
    return [ub_dt , wb_dt]
#I had to put int(ub) to make it stop telling me that I couldn't 
#multiply q_t with ub; hopefully this won't cause problems
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#initial conditions
t0 = 0
ub_dt_at_t0=find_alpha.Ub
wb_dt_at_t0=find_alpha.Wb
#t_final is the solution interval specification
t_final=100
step_size=0.1

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

n_step= math.ceil(t_final/step_size)


#Define Solution Storage Arrays
ub_dt_Eul =np.zeros(n_step+1)
wb_dt_Eul=np.zeros(n_step+1)
t_Eul=np.zeros(n_step+1)

#begin arrays with the initial conditions
ub_dt_Eul[0]=ub_dt_at_t0
wb_dt_Eul[0]=wb_dt_at_t0
t_Eul[0]=t0

#Populating the t array values
for i in range(n_step):
    t_Eul[i+1]=t_Eul[i] + step_size

#And finally, here we use the Euler method on our functions 
for i in range(8):
    [slope_ub_dt,slope_wb_dt]= ubwb_dt(t_Eul[i],ub_dt_Eul[i],wb_dt_Eul[i])
    ub_dt_Eul[i + 1] = ub_dt_Eul[i] + step_size*(slope_ub_dt[i])
    wb_dt_Eul[i+1] = wb_dt_Eul[i] +step_size*(slope_wb_dt[i])
    print(ub_dt_Eul[i],wb_dt_Eul[i])









