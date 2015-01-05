# -*- coding: utf-8 -*-
"""
Created on Wed Dec 24 10:27:22 2014

@author: ydzhao
"""
import picos as pic
import numpy as np

def testLMI():
    Ap = pic.new_param('A', np.eye(3))
    Bp = pic.new_param('B', 2*np.eye(3))
    sdp=pic.Problem()
    Xp = sdp.add_variable('X', (3,3), vtype='symmetric')
    sdp.add_constraint(Xp>>0)
    sdp.add_constraint(Ap*Xp << Bp)
    print sdp
 
    sdp.solve()
    print Xp.value
     
if __name__=="__main__":
    testLMI()
