import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

#Plane coeffecient Data and curve fitting 
delim = "--------------" #adds readability 
alpha = np.array([-16,-12,-8,-4,-2,0,2,4,8,12])
display = True #temporary variable to print the outputs of the curve fit


CD_wing = np.array([
	0.115000000000000 , 0.079000000000000, 0.047000000000000, 0.031000000000000,
 	0.027000000000000, 0.027000000000000, 0.029000000000000, 0.034000000000000, 0.054000000000000, 0.0])

CL_wing = np.array([-1.421000000000000,-1.092000000000000,-0.695000000000000,-0.312000000000000,-0.132000000000000,
 	 0.041000000000000, 0.218000000000000, 0.402000000000000, 0.786000000000000, 1.186000000000000])

CM_wing = np.array([
0.077500000000000, 0.066300000000000, 0.053000000000000, 0.033700000000000, 0.021700000000000,
 0.007300000000000,-0.009000000000000,-0.026300000000000,-0.063200000000000,-0.123500000000000])

# Elevator angle delta_E
delta_el = np.array([-20,-10,0,10,20])

CL_el = np.array([-0.051000000000000,-0.038000000000000, 0, 0.038000000000000, 0.052000000000000])

CM_el = np.array([0.084200000000000, 0.060100000000000,-0.000100000000000,-0.060100000000000,-0.0])
names = np.array(["CD_wing", "CL_wing","CM_wing","CL_el", "CM_el"])
all_arrs = np.array([CD_wing,CL_wing,CM_wing,CL_el,CM_el])

#eh this code could be made better a lot of repeated code here
def plot():
	fig, (ax1,ax2,ax3) = plt.subplots(3, sharex=True)
	ax1.set(ylabel='CD_wing')
	ax1.plot(alpha,CD_wing,'rx')
	ax2.set(ylabel='CL_wing')
	ax2.plot(alpha,CL_wing,'bx')
	ax3.set(ylabel='CM_wing')
	ax3.plot(alpha,CM_wing,'gx')
	fig2, (ax4,ax5) = plt.subplots(2, sharex=True)
	ax4.set(ylabel='CL_el')
	ax4.plot(delta_el,CL_el,'yx')
	ax5.set(ylabel='CM_el')
	ax5.plot(delta_el,CM_el,'cx')
	plt.show()
	

def curve_fit(x,y,name):
	out = np.polyfit(x,y,1,None,False,None,False)
	if(display):
		print("for {}, first value=m,second= c".format(name))
		print(out)
		print(delim)
	return out

def curve_fit_all():
	c_vals = np.array([])
	m_vals = np.array([])
	for i in range(len(all_arrs)):
		if(i < 3):
			temp = curve_fit(alpha,all_arrs[i],names[i])
			c_vals = np.append(c_vals,temp[1]) #is there a better way to do this shit like cmon numpy (i might be dumb)
			m_vals = np.append(m_vals,temp[0])
		else:
			curve_fit(delta_el,all_arrs[i],names[i])
			c_vals = np.append(c_vals,temp[1])
			m_vals = np.append(m_vals,temp[0])
	print(c_vals,m_vals)
	return c_vals,m_vals

def Cl_full(a_in,d_in):
	cs,ms = curve_fit_all()
	return(cs[1] +ms[1]*a_in +ms[4]*d_in)

print(Cl_full(0.4,0.6)) #just a lil test here to see fi we can get some good numbers out of the CL total
# #NOTE: Both of the C values for elevator terms are expected to be zero
# #as their equations take the form y=mx;we'll probably have to use
# #error bounds to discuss why the smaller values found can be
# #dscounted
