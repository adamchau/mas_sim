# -*- coding: utf-8 -*-
"""
Created on Sat Dec 27 17:34:07 2014

@author: ydzhao
"""

import scipy.io as sio
import numpy as np
def pro_mat2py(matdir):
    matdata=sio.loadmat(matdir)
    banlist=['__header__', '__globals__','__version__']
    for item in (set(matdata.keys())-set(banlist)):
        if matdata[item].shape==(1,1):
            matdata[item]=matdata[item].item()
        else:
            matdata[item]=np.matrix(matdata[item])
    return matdata

def pro_py2mat(matdata,matdir):
    for item in matdata.keys():
        if type(matdata[item])==np.ndarray:
            matdata[item]=array(matdata[item].tolist())
        else:
            matdata[item]=array(matdata[item])
            sio.savemat(matdir)
    return matdata

if __name__=="__main__":
    matdir='/home/ydzhao/lmitest.mat'
    matdata=pro_mat2py(matdir)