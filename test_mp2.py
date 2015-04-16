# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 18:54:56 2015

@author: Neutro
"""


import multiprocessing as mp
from Queue import Empty
from classes_var import *
from numpy import array
import time



def locmut(x,nm,Ws,As,COLs,fW,sym=True):
     return( x.goret(nm=3,Ws=Ws,As=As,COLs=COLs,fW=fW,sym=True) )


if __name__ == '__main__':
    W1=[.2,.05,1]
    A1=array([ 0.40325931,  0.09857933,  0.16850174,  0.45300582,  0.32353431, 0.89656194,  0.23588674,  0.41376012,  0.0769273 ,  0.76958047,0.5970651 ,  0.91625161,  0.52238286,  0.99374292,  0.07312555,0.988733  ,  0.18502597,  0.95599975])
    COL1=[125,0,200]
    
    W2=[-.2,.8,-1]
    A2=array([ 0.11397394,  0.97141155,  0.51329606,  0.73262589,  0.76266523,0.30813643,  0.01904868,  0.29648812,  0.8438572 ,  0.25374601,0.6751105 ,  0.88042194,  0.37084719,  0.41668462,  0.68381474,0.20531804,  0.99915379,  0.5396634 ])
    COL2=[125,255,0]
    
    W3=[1,.05,0.002]
    A3=array([ 0.78866611,  0.9736618 ,  0.21897877,  0.48459453,  0.09434612,0.49617057,  0.99932359,  0.52290928,  0.50049834,  0.18727703,0.76507164,  0.82236638,  0.90390197,  0.14742805,  0.20140357,0.41889521,  0.47759195,  0.34418566])
    COL3=[255,0,0]
    
    
    Ws=[W1,W2,W3]
    As=[A1,A2,A3]
    COLs=[COL1,COL2,COL3]
    fW=(.33,.66,1)
    
    
    
    AB=ImagePil(80000)
    AB.printImage
    tdebmut=time.time() 
    AB.mutemV(3,Ws,As,COLs,fW,True)
#    
#    pool= mp.Pool(processes=4)
#    res=[pool.apply_async(locmut, args=(x,3,Ws,As,COLs,fW,True,)) for x in AB.bloc]
#    AB.bloc = [p.get() for p in res]
      
        
    tfinmut=time.time() 
    print(str(tfinmut-tdebmut))
 
   

