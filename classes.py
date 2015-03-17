# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 21:11:58 2015

@author: Dr_Anax

Class Point, Class Image
"""

from __future__ import print_function, division
from numpy import max,random,zeros,nditer,int8
import png
from math import log


class Point:
    """ 
        A point has three attributes: its coordinates (x,y) and its colour(col)
                - The colour is stored in a std list of size 3.
        
        As for now, 3 methods are implemented.
        
        Further work : implement other atractors.
    """
    
    def __init__(self): 
        """
        __init__(self)
            Generates a white point randomly in the [-1:1]² cube.
        """
        self.x,self.y = random.random_sample(2)*2-1
        self.col=[255,255,255]

    def printPoint(self):
        """
        printPoint(self)
            Prints the coordinates and the colour of the considered point.
            
        """
        print(self.x,self.y)
        print(self.col)        
    
    def attractorTriangle(self):
        """
        attractorTriangle(self)
            Mutates the point. The fixed-point of this attractor is Sierpinski’s triangle

        """
        rn=random.random_sample()
        if rn<(1/3):
            self.x/=2
            self.y/=2
            self.col=[(self.col[0]+255)/2,self.col[1]/2,self.col[2]/2]
        elif rn<(2/3):
            self.x=(self.x+1)/2
            self.y/=2
            self.col=[self.col[0]/2,(self.col[1]+255)/2,self.col[2]/2]
        else:
            self.x/=2
            self.y=(self.y+1)/2
            self.col=[self.col[0]/2,self.col[1]/2,(self.col[2]+255)/2]
            
        return self
        
        
        
class Image:
    """
        An image is simply a list of N points.
        
        As for now, 4 methods are implemented:

    """
    def __init__(self,N):
        """
         __init___(self,N)
            Generates N white points randomly in the [-1:1]² cube.
        """
        self.bloc=[Point() for i in range(N)]
        
        
    def mute(self,attractor):
        """
        mute(self,attractor)
            Applies the selected attractor to each point of the image.
        """
        for a in self.bloc:
            attractor(a) 
        
    def printImage(self):
        """
         printImage(self)
            Prints each point (coordinates and colour) of the list. Not recommanded with a large number of points.
        """
        [p.printPoint() for p in self.bloc]
        
        
    def topng(self,sizeImage=500):
        """
        tonpng(self,sizeImage=500) 
            Creates a bitmap that will be used further to create a .png
        """
        bitmap=zeros(shape=(sizeImage,sizeImage*3))
        maxtemp=0
        
        for p in self.bloc: 
            ## for each point we scale the coordinates first
            xpt_mod=int (sizeImage* (p.x+1)/2)
            ypt_mod=3*int (sizeImage* (p.y+1)/2)
            
            ## then each point is put in the bitmap if it's still within the [0,sizeImage] square.           
            if(xpt_mod in range(sizeImage+1) and ypt_mod in range(3*(sizeImage+1))):
                bitmap[xpt_mod][ypt_mod]+=p.col[0]
                bitmap[xpt_mod][ypt_mod+1]+=p.col[1]
                bitmap[xpt_mod][ypt_mod+2]+=p.col[2]
                maxtemp=max((maxtemp,bitmap[xpt_mod][ypt_mod],bitmap[xpt_mod][ypt_mod+1],bitmap[xpt_mod][ypt_mod+2]))
        
        ## the log of this max value is taken.
        lmm=log(maxtemp+1)
       
        ## the colours are then rescaled within [0,255]
        for p in nditer(op=bitmap,op_flags=["readwrite"]):
            p[...]=int(255*log(1+p)/lmm)
              
        return bitmap           