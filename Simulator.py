import numpy as np
import matplotlib.pyplot as plt
import Aircraft
import math
class Simulator():
    def __init__(self,sim_conditions):
        self.time_step = 0.01
        self.sim_conditions = sim_conditions
        aircraft_conditions = {"Velocity" : self.sim_conditions.get("Velocity"),"Thrust" : self.sim_conditions.get("Thrust"),  "Flight Path" : self.sim_conditions.get("Flight Path"), "Time Step" : self.time_step}
        self.plane = Aircraft.Aircraft(aircraft_conditions)
        self.steps = math.ceil(self.sim_conditions.get("Run Time")/self.time_step)
        self.t_ret = np.array([])
        self.gamma_ret = np.array([])
        self.alpha_ret = np.array([])
        self.ub_ret = np.array([])
        self.wb_ret  = np.array([])
        self.theta_ret = np.array([])
        self.delta_ret = np.array([])
        self.altitude_ret = np.array([])
    def set_initials(self):
        self.plane.set_initials()
        print("Initial conditions: ", self.plane.fetch_state())
    def cycles(self):
        for i in range(self.steps):
            self.plane.get_derivatives()
            self.plane.update_state()
            self.t_ret = np.append(self.t_ret,i * self.time_step)
            self.gamma_ret = np.append(self.gamma_ret,math.degrees(self.plane.gamma))
            self.alpha_ret = np.append(self.alpha_ret,math.degrees(self.plane.alpha))
            self.ub_ret = np.append(self.ub_ret,self.plane.ub)
            self.wb_ret = np.append(self.wb_ret,self.plane.wb)
            self.delta_ret = np.append(self.delta_ret,self.plane.delta_el)
            self.altitude_ret = np.append(self.altitude_ret,-self.plane.z_e)
            self.theta_ret = np.append(self.theta_ret,math.degrees(self.plane.theta))
            if i  >= (self.sim_conditions.get("Elevator Time") * 100):
                self.plane.del_mod = (1 + (self.sim_conditions.get("Elevator Change")/100.0))
            if i  >= (self.sim_conditions.get("Thrust Time") * 100):
                self.plane.Thrust_mod = (1 + (self.sim_conditions.get("Thrust Change")/100.0))
            if self.plane.z_e <= -2000:
                self.plane.del_mod = 1
                self.plane.gamma = 0
            """
            part b 2
            if self.plane.z_e <= -2000:
                self.plane.del_mod = 1
                print((i / 100) - 10)
                break
                self.plane.gamma = 0
            """
                
        fig, (ax1,ax2,ax3) = plt.subplots(3, sharex=True)
        ax1.set(ylabel='alpha (deg)',xlabel = 'Time, t(s)')
        ax1.plot(self.t_ret,self.alpha_ret,'r--')
        ax2.set(ylabel='gamma (deg)',xlabel = 'Time, t(s)')
        ax2.plot(self.t_ret,self.gamma_ret,'b--')
        ax3.set(ylabel='theta (deg)',xlabel = 'Time, t(s)')
        ax3.plot(self.t_ret,self.theta_ret,'g--')
        fig2, (ax4,ax5,ax6) = plt.subplots(3, sharex=True)
        ax4.set(ylabel='ub (m/s)',xlabel = 'Time, t(s)')
        ax4.plot(self.t_ret,self.ub_ret,'y--')
        ax5.set(ylabel='wb (m/s)',xlabel = 'Time, t(s)')
        ax5.plot(self.t_ret,self.wb_ret,'c--')
        ax6.set(ylabel='Altitude(m/s)',xlabel = 'Time, t(s)')
        ax6.plot(self.t_ret,self.altitude_ret,'k--')
        return fig,fig2
