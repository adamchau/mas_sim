# -*- coding: utf-8 -*-
"""
Created on Wed Oct 22 09:07:07 2014

@author: ydzhao
"""
from mas_sys import *
import spyderlib.utils.iofuncs as sui

if __name__=="__main__":
        sui.save_session('simspy.spydata')
        plt.close('all')
        t_start=0
        t_end=sim_times
        energy=cal_energy(MAS1,sim_times,T_intval)
        print energy
        plt.figure()
        nx.draw(MAS1.G, with_labels = True)
        def plot_mas():
            '''
                1.  mas consensus
            '''
            plt.figure()
            for i in range(MAS1.agent_num):
                agent1_var=[data[i][0,0] for data in MAS1.status_his]
                plt.plot(MAS1.T[t_start:t_end],agent1_var[t_start:t_end])
        
        def plot_ev_mas_cen():        
            '''
                2.  event-triggered consensus
            '''
            plt.figure()
            plt.subplot(2,2,1)
            for i in range(ev_MAS1.agent_num):
                agent1_var=[data[i] for data in ev_MAS1.status_his]
                plt.plot(ev_MAS1.T[t_start:t_end],agent1_var[t_start:t_end])
            '''
                    2.1 event-triggered error dynamics
            '''

            '''
                    2.2 event-triggered triggered time
            '''            
            plt.subplot(2,2,2)
            plt.plot(ev_MAS1.T[t_start:t_end],ev_MAS1.error_his[t_start:t_end])
            plt.plot(ev_MAS1.T[t_start:t_end],ev_MAS1.bound_his[t_start:t_end])
            plt.subplot(2,2,3)
            plt.ylim(0,1.6)
            triggered=[]
            for t in ev_MAS1.T:
                if t in ev_MAS1.triggeredT:
                    triggered.append(1)
                else:
                    triggered.append(0)               
            plt.plot(ev_MAS1.T[t_start:t_end],triggered[t_start:t_end])
            
        def plot_ev_mas_dis():
            plt.figure()
            plt.subplot(2,2,1)
            for i in range(ev_dis_MAS1.agent_num):
                agent1_var=[data[i] for data in ev_dis_MAS1.status_his]
                plt.plot(ev_dis_MAS1.T[t_start:t_end],agent1_var[t_start:t_end])
            
            plt.subplot(2,2,2)
            i=2
            error1_his=[e[i] for e in ev_dis_MAS1.error_his]
            bound1_his=[h[i] for h in ev_dis_MAS1.bound_his]
            plt.plot(ev_dis_MAS1.T[t_start:t_end],error1_his)
            plt.plot(ev_dis_MAS1.T[t_start:t_end],bound1_his)
            
            plt.subplot(2,2,3)
            plt.ylim(0,1.6)
            triggered=[]
            for t in ev_MAS1.T:
                if t in ev_MAS1.triggeredT:
                    triggered.append(1)
                else:
                    triggered.append(0)               
            plt.plot(ev_MAS1.T[t_start:t_end],triggered[t_start:t_end])

            
        switch_dict={1:plot_mas,2:plot_ev_mas_cen,3:plot_ev_mas_dis}
        switch_dict[1]()
            
        
        