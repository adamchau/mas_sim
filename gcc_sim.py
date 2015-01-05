# -*- coding: utf-8 -*-
"""
Created on Sat Dec 27 18:47:05 2014

@author: ydzhao
"""
if __name__=="__main__":
    MAS1=mas_sys(agent_list,topology)
    sim_times=1000
    for N in range(sim_times):
        MAS1.mas_pro_applied(0.01)