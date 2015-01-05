# -*- coding: utf-8 -*-
"""
Created on Fri Dec 26 16:09:52 2014

@author: ydzhao
"""

import sympy as spy
spy.init_printing(use_unicode=True)
a1=spy.symbols('a1')
a2=spy.symbols('a2')
a3=spy.symbols('a3')
a4=spy.symbols('a4')
a5=spy.symbols('a5')
deltaA=spy.Matrix([[-0.04743*a1,0,0,0,0,0,0,0,0,0],\
[0,-0.0763*a2,0,0,0,0,0,0,0,0],\
[0,0,0,0,0,0,0,0,0,0],\
[0,0,0,0,0,0,0,0,0,0],\
[0,-0.017408*a3,0,0,0,0,0,0,0,0],\
[-0.008981*a4,-0.28926*a5,0,0,0,0,0,0,0,0],\
[0,0,0,0,0,0,0,0,0,0],\
[0,0,0,0,0,0,0,0,0,0],\
[0,0,0,0,0,0,0,0,0,0],\
[0,0,0,0,0,0,0,0,0,0]])



