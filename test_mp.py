# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 15:49:23 2015

@author: Neutro
"""


from classes_var_config import *
from numpy import array
import time
import config




if __name__ == '__main__':
    
    
    
    AB=ImagePil(800)
    tdebmutser=time.time() 
    #AB.mutemV(nm,Ws,As,COLs,fW,True,False)
    AB.mutemV(False)
    tfinser=time.time()
    print 'temps pas parallele: %s' % str(tfinser-tdebmutser)
    
    
    AB=ImagePil(800)
    print 30 * '-'
    print 'Process in parallel ...' 
    debpar = time.time()
    #AB.mutemV(nm,Ws,As,COLs,fW,True,True)
    AB.mutemV(True)
    finpar = time.time()    
    print 'temps parallele: %s' % str(finpar-debpar)

      

   

