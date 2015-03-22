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
from classes import *
import copy
import os
import time
import operator


def blobend(s,nbpt,reps):
    
    if not os.path.exists("BlobTimed"):
        os.makedirs("BlobTimed")
   
    t_beforepng=[]
    t_postpng=[]
    t_towrite=[]
    t_postmuteA=[]
    t_postcopyB=[]
    t_postmuteB=[]
       
    
    t_beforegen=time.time()         
    A=ImagePil(nbpt)
    t_postgen=time.time()   
    B=copy.deepcopy(A)
    t_postcopy=time.time()
    B.mute(Point.attractorBlob,high=2,low=-2,waves=13)
    t_mutationblob=time.time()
    
        
    
    for i in range(reps):
        t_beforepng.append(time.time())
        t=B.toImage(s)
        t_postpng.append(time.time())
        thong="BlobTimed/figure"+str(i+10)+".png"         
        t.save(thong) 
        t_towrite.append(time.time())
        if (i != reps-1):
           A.mute(Point.attractorTriangle)
           
           t_postmuteA.append(time.time())
           
           B=copy.deepcopy(A)
           
           t_postcopyB.append(time.time())
           
           B.mute(Point.attractorBlob,high=2,low=-2,waves=13)
           
           t_postmuteB.append(time.time())
          
    return (t_beforegen,t_postgen,t_postcopy,t_mutationblob,t_beforepng,t_postpng,t_towrite,t_postmuteA, t_postcopyB, t_postmuteB)
    
###########################
### Starting the program
###########################
    
start_time = time.time()   
s=1020
nbpt=500000
reps=30
t_beforegen,t_postgen,t_postcopy,t_mutationblob,t_beforepng,t_postpng,t_towrite,t_postmuteA, t_postcopyB, t_postmuteB=blobend(s,nbpt,reps)  
t_end=time.time()

#### some operations on times
t_png=map(operator.sub,t_postpng,t_beforepng)
t_write=map(operator.sub,t_towrite,t_postpng)
del t_towrite[reps-1] # safer than [-1]
t_muteA=map(operator.sub,t_postmuteA,t_towrite)
t_copyB=map(operator.sub,t_postcopyB,t_postmuteA) # actually A is copied. anyhow.
t_muteB=map(operator.sub, t_postmuteB,t_postcopyB) 


os.chdir("BlobTimed")      
os.system("convert *png animation.gif")

f = open("log.txt", 'a+') ## beware as it will write at the end of the current file
print("- Parameters:",file=f)
print("    -s=%s" %s,file=f)
print("    -nbpt=%s" %nbpt,file=f)
print("    -reps=%s" %reps,file=f)


print("\n-Total execution time:  %s seconds ---" % (t_end - start_time),file=f)
print(" -Details: ",file=f)
print("   -Generation of the first image A: " + str(t_postgen-t_beforegen) + " seconds",file=f)
print("   -Time to copy the first image (create B): "+str(t_postcopy-t_postgen) +" seconds ",file=f) 
print("   -Time to mute the first B: "+str(t_mutationblob - t_postcopy)+" seconds ",file=f) 

print("\n -Some means: ",file=f)
print("   - Mean time of the toImage operation: "+str(numpy.mean(t_png))+" seconds",file=f)
print("   - Mean time of the writing operation: "+str(numpy.mean(t_write))+" seconds",file=f)
print("   - Mean time of the A mutation (Serps'): "+str(numpy.mean(t_muteA))+" seconds",file=f)
print("   - Mean time of the B copy: "+str(numpy.mean(t_copyB))+" seconds",file=f)
print("   - Mean time of the blob filter (muteB): "+str(numpy.mean(t_muteB))+" seconds",file=f)
f.close()

