# -*- coding: utf-8 -*-
"""
Created on Tue Oct 21 15:17:13 2014

@author: ydzhao
"""

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import control as control
import networkx as nx

class mas_sys:
    def __init__(self,agent_list,topology,di,pro_para=[1,-10]):
        self.agent_list=agent_list # agent model list
        self.agent_num=len(agent_list) # num of agents
        self.G=topology # communication graph
        self.L=nx.laplacian_matrix(self.G) # graph l       self.L=nx.laplacian_matrix(self.G) Laplacian
        self.A=nx.adjacency_matrix(self.G) # adjancency matrix
        self.init_state=[np.matrix(ag.state) for ag in agent_list] # MAS initial states
        self.status=self.init_state
        self.t=0   # initial states
        self.T=[0]  # time label
        self.status_his=[self.status] # states history
        self.input_his=[]
      #  self.input_his=[self.input] # protocol histroy
        self.neighbor_set=[] # neighbor set for every agents
        for node_i in range(self.agent_num):
            self.G.node[node_i]=self.agent_list[node_i]
            i_node_neighbor_list=[n for n in self.G[node_i]]
            self.neighbor_set.append(i_node_neighbor_list)
        self.di=di
        self.c=pro_para[0]
        self.K=pro_para[1]
            
    def draw_mas_sys(self):
        plt.figure()
        nx.draw_networkx(self.G)
        
    def mas_protocol(self,i):
        '''
        使用协议
        '''
        u=0
        x=self.status_2states()
        for j in range(self.agent_num):
            u+=self.A[i,j]*(x[i]-x[j])
        u+=self.di[i]*x[i]
        u=self.c*self.K*u
        return u
        
    def status_2states(self):
        x=np.zeros(self.agent_num).tolist()
        for m in range(self.agent_num):
            x[m]=np.matrix(self.status[m])
        return x
    
    def status_2agg(self):
        agglist=[]
        for m in range(self.agent_num):
            agglist+=self.status[m].transpose().tolist()[0]
        return np.matrix(agglist).transpose()
        
    def vec_2agg(self,vec):
        agglist=[]
        for m in range(self.agent_num):
            agglist+=vec[m].transpose().tolist()[0]
        return np.matrix(agglist).transpose()
    
    def agg_2vec(self,agg):
        veclist=[]
        n=agg.shape[0]/self.agent_num
        for m in range(self.agent_num):
            veclist.append(agg[m*n:(m+1)*n])
        return veclist
            
    def update_mas_status(self):
        self.status=[self.G.node[i].state for i in range(self.agent_num)]
        
    def agent_u_applied(self,i,T_intval):
        ui=self.mas_protocol(i)
        self.G.node[i].input_sim(ui,T_intval)
        return ui
    
    def mas_pro_applied(self,T_intval):
        uinput=[]
#        x=self.status_2agg()
#        uagg=self.c*sp.kron(self.L+sp.diag(self.di),self.K)*x
#        uagglist=self.agg_2vec(uagg)
#        for i in range(self.agent_num):
#            ui=uagglist[i]
#            self.G.node[i].input_sim(ui,T_intval)
#            uinput.append(ui)
        for i in range(self.agent_num):
           ui=self.mas_protocol(i)
           uinput.append(ui)
        for i in range(self.agent_num):
            self.G.node[i].input_sim(uinput[i],T_intval)        

#        uiagg=self.vec_2agg(uinput)
#        err=np.linalg.norm (np.round((uagg-uiagg)*10000))
#        print err==0
           
        self.t+=T_intval
        self.T.append(self.t)
        self.update_mas_status()
        self.status_his.append(self.status)
        self.input_his.append(uinput)
        
class mas_agent:
    def __init__(self,A=0,B=1,C=1,D=0,x0=1):
        self.agent_model=control.ss(A,B,C,D)
        self.x0=x0
        self.state=x0
        
    def input_sim(self,u=0,T_intval=0.01):
        u=u.transpose()
        u=np.array([u.tolist()[0],u.tolist()[0]]).transpose()
        T, yout, xout=control.forced_response(self.agent_model, np.array([0,T_intval]),u, self.state)
        self.state=np.matrix(np.array(xout).transpose()[-1]).transpose()

def create_graph_from_laplacian(L):
    D=np.matrix(np.diag(np.diag(L)))
    A=D-L
    G=nx.from_numpy_matrix(A)
    return G
    
def ag_matrixlist(slist):
    x=[]
    for i in range(len(slist)):
        x+=slist[i].transpose().tolist()[0]
    return np.matrix(x).transpose()

def  cal_energy(MAS1,times,T_intval):
        D=sp.diag(MAS1.di)
        L=MAS1.L+D
        Q=sp.kron(L,sp.eye(MAS1.status[0].shape[0]))
        R=sp.kron(sp.eye(MAS1.agent_num),sp.eye(MAS1.input_his[0][0].shape[0]))
        energy=0
        for t in range(times):
            x=ag_matrixlist(MAS1.status_his[t])
            u=ag_matrixlist(MAS1.input_his[t])
            delta=(x.transpose()*Q*x+u.transpose()*R*u)*T_intval
            energy+=delta
        return energy.item()
        
        

if __name__=="__main__":
    L=np.matrix([[1,-1,0,0],[-1,3,-1,-1],[0,-1,2,-1],[0,-1,-1,2]])
    topology=create_graph_from_laplacian(L)
    agent1=mas_agent(0,1,1,0,-1)
    agent2=mas_agent(0,1,1,0,2)
    agent3=mas_agent(0,1,1,0,3)
    agent4=mas_agent(0,1,1,0,-4)
    agent_list=[agent1,agent2,agent3,agent4]
    MAS1=mas_sys(agent_list,topology,di=np.zeros(len(agent_list)))
    sim_times=100
    for N in range(sim_times):
        MAS1.mas_pro_applied(0.01)
