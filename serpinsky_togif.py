# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 12:05:41 2015

@author: Dr_Anax

Another simple and slow implementation of flames fractals: http://flam3.com/flame_draves.pdf


"""
from classes import *
import os 
        
def serp():           
    s=1020            
    A=Image(500000)
    for i in range(20):
        t=A.topng(s) 
        thong="figure"+str(i+10)+".png"         
        f = open(thong,'wb')
        w = png.Writer(s,s)
        w.write(f, t)  
        f.close()     
        if (i != 19):
            A.mute(Point.attractorTriangle)
            
serp()        
os.system("convert *png animation.gif") 