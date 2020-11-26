from scipy import optimize
import numpy as np
#Plane coeffecient Data
#container for data and related coeffecient things
#initial guesses
CL_0 = 0.0410
CL_alpha = 0.1
CL_delta = 0.003
CD_0 = 0.026
CD_k = 0.045
CM_0 = 0.007
CM_alpha = -0.01
CM_delta = -0.004
all_guess = np.array([(CL_0,CL_alpha),CL_delta,(CD_0,CD_k),(CM_0,CM_alpha),CM_delta])

#------Data Values--------
alpha = np.array([-16,-12,-8,-4,-2,0,2,4,8,12])
delta_el  = np.array([-20,-10,0,10,20])

CD = np.array([
    0.115000000000000
  , 0.079000000000000
  , 0.047000000000000
  , 0.031000000000000
  , 0.027000000000000
  , 0.027000000000000
  , 0.029000000000000
  , 0.034000000000000
  , 0.054000000000000
  , 0.089000000000000
  ])


CL = np.array([
   -1.421000000000000
  ,-1.092000000000000
  ,-0.695000000000000
  ,-0.312000000000000
  ,-0.132000000000000
  , 0.041000000000000
  , 0.218000000000000
  , 0.402000000000000
  , 0.786000000000000
  , 1.186000000000000
  ])

CM = np.array([
    0.077500000000000
  , 0.066300000000000
  , 0.053000000000000
  , 0.033700000000000
  , 0.021700000000000
  , 0.007300000000000
  ,-0.009000000000000
  ,-0.026300000000000
  ,-0.063200000000000
  ,-0.123500000000000
  ])

CL_el = np.array([
   -0.051000000000000
  ,-0.038000000000000
  ,                 0
  , 0.038000000000000
  , 0.052000000000000
  ])

CM_el = np.array([
    0.084200000000000
  , 0.060100000000000
  ,-0.000100000000000
  ,-0.060100000000000
  ,-0.084300000000000
  ])

names = np.array(["CD_wing", "CL_wing","CM_wing","CL_el", "CM_el"])
all_arrs = np.array([CD,CL,CM,CL_el,CM_el])
feed = np.array([(alpha, CL),(delta_el,CL_el),(CL,CD),(alpha,CM),(delta_el,CM_el)])
#-----------Functions------ 
def CL_a_func(x, a, b): #alpha, cl
    return a + b * x
def CL_d_func(x, a): #delta_el, CL_el
    return a * x
def CD_CL_func(x, a, b): #CL, CD
    return a + b * x**2.0
def CM_alpha_func(x, a, b): #alpha,CM
    return a + b * x
def CM_d_func(x, a): #delta_el, CM_el
    return a * x
#-----------------------
all_funcs = np.array([CL_a_func,CL_d_func,CD_CL_func,CM_alpha_func,CM_d_func])

#uses scipy to curve fit
def curve_fit_all():
    all_covars = np.array([])
    all_params = np.array([])
    for i in range(len(all_funcs)):
        params,covars = optimize.curve_fit(all_funcs[i],feed[i][0],feed[i][1],all_guess[i])
        all_covars = np.append(all_covars,covars)
        all_params = np.append(all_params,params)
    return all_params,all_covars
# create a dictionary of all the coeffecients so that they can be accessed easily
# calling set_coeffecients will call curve_fit_all and returns the coeffecients and covariance
def set_coeffecients():
    coeffs,covar = curve_fit_all()
    coeffecients = {'CL_0' : coeffs[0], "CL_alpha" : coeffs[1],"CL_delta" : coeffs[2],"CD_0" : coeffs[3],"CD_K" : coeffs[4],"CM_0" : coeffs[5],"CM_alpha" : coeffs[6], "CM_delta" : coeffs[7]}
    covariance = {"CL_0" : covar[0],"CL_alpha" : covar[1],"CL_delta" : covar[2],"CD_0" : covar[3],"CD_K" : covar[4],"CM_0" : covar[5],"CM_alpha" : covar[6], "CM_delt" : covar[7]}
    return coeffecients,covariance

