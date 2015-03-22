# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 21:11:58 2015

@author: Dr_Anax

Class Point, Class Image
"""

from __future__ import print_function, division
from numpy import max,random,zeros,sign
from PIL import Image
from math import log,sqrt,atan,sin,cos


    
    
def rescale255(tuple_bm3,rha):
    ## Ugly. will fix that later.
    a=int(tuple_bm3[0]*rha)
    b=int(tuple_bm3[1]*rha)
    c=int(tuple_bm3[2]*rha)
    return (a,b,c)
    

class Point:
    """ 
        A point has three attributes: its coordinates (x,y) and its colour(col)
                - The colour is stored in a tuple of size 3.
        
        As for now, 4 methods are implemented.
        
        Further work : implement other atractors.
    """
    
    def __init__(self): 
        """
        __init__(self)
            Generates a white point randomly in the [-1:1]² cube.
        """
        self.x,self.y = random.random_sample(2)*2-1
        self.col=(255,255,255)

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
            self.col=map(int,((self.col[0]+255)/2,self.col[1]/2,self.col[2]/2))
        elif rn<(2/3):
            self.x=(self.x+1)/2
            self.y/=2
            self.col=map(int,(self.col[0]/2,(self.col[1]+255)/2,self.col[2]/2))
        else:
            self.x/=2
            self.y=(self.y+1)/2
            self.col=map(int,(self.col[0]/2,self.col[1]/2,(self.col[2]+255)/2))
            
        return self
        
    def attractorBlob(self,high,low,waves):
        """
        attractorBlob(self)
            Mutates the point. 
            The fixed-point of this attractor is a blob (see #23 on the paper). No colour modification is applied.
            NB: actually, applying the blob attractor more than once forces the convergence toward the [0,0] point.
                For this reason, the blob attracor should be used as an final filter.

        """
        r= sqrt(self.x*self.x+self.y*self.y)
        if (self.y != 0):
            theta=atan(self.x/self.y)
        else :
            theta=sign(self.x)
        cst=r*(low+(high-low)/2*(sin(waves*theta)+1))
        self.x=r*cst*cos(theta)
        self.y=r*cst*sin(theta)
        
        return self    
        
        
class ImagePil:
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
        
        
    def mute(self,attractor,**kwargs):
        """
        mute(self,attractor)
            Applies the selected attractor to each point of the image.
        """
        for a in self.bloc:
            attractor(a,**kwargs) 
        
    def printImage(self):
        """
         printImage(self)
            Prints each point (coordinates and colour) of the list.
            Not recommanded with a large number of points.
        """
        [p.printPoint() for p in self.bloc]
        
    

    
    def toImage(self,sizeImage=500):
        """
        tonpng(self,sizeImage=500) 
            Creates an Image using pillow
        """
        img = Image.new( 'RGB', (sizeImage,sizeImage), "black")
        bitmap = img.load()
        intensity=zeros((sizeImage,sizeImage))        
                
        
        for p in self.bloc: 
            ## for each point we scale the coordinates first
            xpt_mod=int (sizeImage* (p.x+1)/2)
            ypt_mod=int (sizeImage* (p.y+1)/2)
            
            ## then each point is put in the bitmap if it's still within the [0,sizeImage] square.           
            if(xpt_mod in range(sizeImage) and ypt_mod in range(sizeImage)):
                intensity[xpt_mod,ypt_mod]+=1
                bitmap[xpt_mod,ypt_mod]=tuple(map(lambda x, y: int((x + y)/2), bitmap[xpt_mod,ypt_mod],p.col))
                
        
        ## 
        lmm=log(max(intensity)+1)
       
        ## the colours are then rescaled within [0,255]
        for i in range(sizeImage):    
            for j in range(sizeImage):
                rha= log(intensity[i,j]+1)/lmm
                bitmap[i,j]=rescale255(bitmap[i,j],rha)
              
        return img         
    