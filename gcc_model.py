# -*- coding: utf-8 -*-
"""
Created on Sat Dec 27 18:45:53 2014

@author: ydzhao
"""
import data_converter as dc
from mas_sys import *
import processbar as pb
import spyderlib.utils.iofuncs as sui 
if __name__=="__main__":
    matdir='lmitest2.mat'
    matdata=dc.loadmat(matdir)
    A,B,C,D,E,n,m,N,x10,x20,x30,Q,R,LG,Di,X_sol,W_sol,c,K,J=matdata['A'],matdata['B'],\
    matdata['C'],matdata['D'],matdata['E'],matdata['n'],matdata['m'],matdata['N'],\
    matdata['x10'],matdata['x20'],matdata['x30'],matdata['Q'],matdata['R'],matdata['LG'],\
    matdata['Di'],matdata['X_sol'],matdata['W_sol'],matdata['cp'],matdata['K'],matdata['J']
    di=[Di[0,i] for i in range(N)]    
    L=LG
    topology=create_graph_from_laplacian(L)
    Du=np.zeros(B.shape)
    agent1=mas_agent(A,B,C,Du,x10.transpose())
    agent2=mas_agent(A,B,C,Du,x20.transpose())
    agent3=mas_agent(A,B,C,Du,x30.transpose())
    agent_list=[agent1,agent2,agent3]
    MAS1=mas_sys(agent_list,topology,di,pro_para=[c,K])
    t_bar=pb._start_progress()
    count=0
    sim_times=10000
    T_intval=0.00005
    for N in range(sim_times):
        pb._set_progress(t_bar,count*100/sim_times)  
        MAS1.mas_pro_applied(T_intval)
        count+=1
    pb._stop_progress(t_bar)
    print "Done!"
    sui.save_session('simspy.spydata')