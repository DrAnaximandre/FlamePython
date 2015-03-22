# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 12:05:41 2015

@author: Dr_Anax

Another simple and slow implementation of flames fractals: http://flam3.com/flame_draves.pdf

This file creates a nice Serp's triangle gif.
It illustrates the convergence of the repetitively iterated attractor to points that are randomly sampled in the [-1;1]²;

This is quite slow, on my machine it takes ~13 minutes.
"""
from classes import *
import os 

        
def serp():  
        
    if not os.path.exists("Serp"):
        os.makedirs("Serp")
         
    s=1020           
    A=ImagePil(500000)
    for i in range(30):
        t=A.toImage(s)
        thong="Serp/figure"+str(i+10)+".png"         
        t.save(thong) 
        if (i != 29):
            A.mute(Point.attractorTriangle)
       
            
            
            
serp()    
os.chdir("Serp")     
os.system("convert *png animation.gif") 