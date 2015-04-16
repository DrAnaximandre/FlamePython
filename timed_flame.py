# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 22:21:55 2015

@author: Dr_Anax

This file generates 30 images of the Serp's triangle on which are applied a "blob" filter.
Then the blobbed images are written in png, and a gif is generated.
The operations are timed, and a log file is written.

The whole experiment took 18 minutes on my PC.

As one can see, the ImagePil.toImage method is the longest operation (~20s), followed by the copy.deepcopy operation (~15s).
The mutation (and thus blobbing) is "not so long" (~1s).
Writing is also quite fast compared to the other methods.

Will try to improve the timings in a next update.
"""

from __future__ import print_function, division
from classes_var import *
import copy
import os
import time
import operator
from numpy import array


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
#

def blobend(s,nbpt,reps):
    
    if not os.path.exists("Timed"):
        os.makedirs("Timed")
   
    t_beforepng=[]
    t_postpng=[]
    t_towrite=[]
    t_postmuteA=[]
       
    
    t_beforegen=time.time()         
    A=ImagePil(nbpt)
    t_postgen=time.time()   
  
    for i in range(reps):
        t_beforepng.append(time.time())
        t=A.toImage(s)
        t_postpng.append(time.time())
        thong="Timed/figure"+str(i+10)+".png"         
        t.save(thong) 
        t_towrite.append(time.time())
        if (i != reps-1):
           A.mutemV(3,Ws,As,COLs,fW,True)
           t_postmuteA.append(time.time())
      
    return (t_beforegen,t_postgen,t_beforepng,t_postpng,t_towrite,t_postmuteA)
    
###########################
### Starting the program
###########################
    
start_time = time.time()   
s=1020
nbpt=500000
reps=10
t_beforegen,t_postgen,t_beforepng,t_postpng,t_towrite,t_postmuteA=blobend(s,nbpt,reps)  
t_end=time.time()

#### some operations on times
t_png=map(operator.sub,t_postpng,t_beforepng)
t_write=map(operator.sub,t_towrite,t_postpng)
del t_towrite[reps-1] # safer than [-1]
t_muteA=map(operator.sub,t_postmuteA,t_towrite)



os.chdir("Timed")      
os.system("convert *png animation.gif")

f = open("log.txt", 'a+') ## beware as it will write at the end of the current file
print("- Parameters:",file=f)
print("    -s=%s" %s,file=f)
print("    -nbpt=%s" %nbpt,file=f)
print("    -reps=%s" %reps,file=f)


print("\n-Total execution time:  %s seconds ---" % (t_end - start_time),file=f)
print(" -Details: ",file=f)
print("   -Generation of the first image A: " + str(t_postgen-t_beforegen) + " seconds",file=f)

print("\n -Some means: ",file=f)
print("   - Mean time of the toImage operation: "+str(numpy.mean(t_png))+" seconds",file=f)
print("   - Mean time of the writing operation: "+str(numpy.mean(t_write))+" seconds",file=f)
print("   - Mean time of the A mutation : "+str(numpy.mean(t_muteA))+" seconds",file=f)

f.close()

