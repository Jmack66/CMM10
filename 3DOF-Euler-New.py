import find_alpha as fa
import vehicle
import env
import math as math
import numpy as np
import matplotlib.pyplot as plt
import CoeffecientData as cd

t0 = 0
q = 0
ub_local = fa.Ub
wb_local = fa.Wb
ub_stack = np.zeros(1000)
wb_stack = np.zeros(1000)
run_time = np.zeros(1000)
W=fa.W
m = vehicle.acMass
time = np.linspace(0,1000,1) #we are time stepping from 0 to 100 seconds at centisecond increments where a value in an array is at a time step of 100ms
#get new alpha based on last alpha
alpha_stack = np.zeros(1000)
al = fa.solve_alpha(0)
alpha_stack[0] = al[0]
coef,covar = cd.set_coeffecients()
def euler_method(F,x0,y0,h,x):
        y = 0
        ys = np.array([])
        while x0 < x:
            y = y + h * F(y, x0)
            ys = np.append(ys,y)
            x0 = x0 + h
        return ys
    #page 5 lecture 9
def ubwb_dt(q,ub,wb,alpha_s,T,D,L):
    ub_dt= (L/m)*math.sin(alpha_s)-(D/m)*math.cos(alpha_s)\
        -(q)*(wb) -(W/m)*math.sin(alpha_s)+ (T/m)
    wb_dt = -(L/m)*math.cos(alpha_s)-(D/m)* math.sin(alpha_s)\
        +(q)*(ub) +(W/m)*math.cos(alpha_s)
    return ub_dt , wb_dt

def q_dt(M):
    dq_dt = M/(vehicle.inertia_yy)
    return dq_dt

for i in range(100):
    run_time[i] = i
    alpha_current = fa.solve_alpha(alpha_stack[int(i) - 1])
    alpha_stack[int(i)] = alpha_current[0]
    print(alpha_current[0])
    CL_local,CM_local,CD_local = cd.get_current_coeffecients(alpha_current)
    L = 0.5*(env.air_density)*(fa.V**2)*(vehicle.Sref)*(CL_local)
    D = 0.5*(env.air_density)*(fa.V**2)*(vehicle.Sref)*(CD_local)
    M = 0.5*(env.air_density)*(fa.V**2)*(vehicle.Sref)*(vehicle.cbar)*(CM_local)
    T = fa.get_thrust(alpha_current)
    q += q_dt(M)
    ub_temp,wb_temp = ubwb_dt(q,ub_local,wb_local,alpha_current,T,D,L)
    ub_local += ub_temp
    wb_local += wb_temp
    ub_stack[int(i)] = ub_local
    wb_stack[int(i)] = wb_local


plt.plot(run_time,ub_stack,'r--')
plt.show()