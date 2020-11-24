from scipy import optimize
import numpy as np
import matplotlib.pyplot as plt
import CoeffecientData as cd

display = True
delim = "--------------" #adds readability
#Curve fit using Poly fit unsure if we still want this
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
	for i in range(len(cd.all_arrs)):
		if(i < 3):
			temp = curve_fit(cd.alpha,cd.all_arrs[i],cd.names[i])
			c_vals = np.append(c_vals,temp[1])
			m_vals = np.append(m_vals,temp[0])
		else:
			temp = curve_fit(cd.delta_el,cd.all_arrs[i],cd.names[i])
			c_vals = np.append(c_vals,temp[1])
			m_vals = np.append(m_vals,temp[0])
	return c_vals,m_vals

def Cl_full(a_in,d_in):
	cs,ms = curve_fit_all()
	return(cs[1] +ms[1]*a_in +ms[4]*d_in)
#-----------------------------------------
#wrapper function for scipy curve fit 
def curve_fit_sci(func,x,y,ip):
	params, params_covariance = optimize.curve_fit(func,x, y,
        p0=ip)
	return params, params_covariance
def curve_fit_all_sci():


def plot():
	fig, (ax1,ax2,ax3) = plt.subplots(3, sharex=True)
	ax1.set(ylabel='CD_wing')
	ax1.plot(cd.alpha,cd.CD_wing,'rx')
	ax2.set(ylabel='CL_wing')
	ax2.plot(cd.alpha,cd.CL_wing,'bx')
	ax3.set(ylabel='CM_wing')
	ax3.plot(cd.alpha,cd.CM_wing,'gx')
	fig2, (ax4,ax5) = plt.subplots(2, sharex=True)
	ax4.set(ylabel='CL_el')
	ax4.plot(cd.delta_el,cd.CL_el,'yx')
	ax5.set(ylabel='CM_el')
	ax5.plot(cd.delta_el,cd.CM_el,'cx')
	plt.show()
