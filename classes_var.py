# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 21:11:58 2015

@author: Dr_Anax

Class Point, Class Image
"""

from __future__ import print_function, division

import multiprocessing
from numpy import max,random,zeros
from PIL import Image
from math import log,sqrt,sin,cos
import time
import config


N_JOBS = -1
  
    
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
    
    
    def F(self,W,A,COL):
        x=self.x
        y=self.y        
        x_new=[0,0,0]       
        y_new=[0,0,0] 
        r=sqrt(x*x+y*y)
        
        ## Linear attractor
        x_new[0]=A[0]*x+A[1]*y+A[2]
        y_new[0]=A[3]*x+A[4]*y+A[5]
        
        ## Sinusoidal attractor
        x_new[1]=sin(A[6]*x+A[7]*y+A[8])
        y_new[1]=sin(A[9]*x+A[10]*y+A[11])
        
        ## swirl attractor
        x_t=A[12]*x+A[13]*y+A[14]
        y_t=A[15]*x+A[16]*y+A[17]
        x_new[2]=x_t*sin(r*r)-y_t*cos(r*r)
        y_new[2]=x_t*cos(r*r)+y_t*sin(r*r)
         
        
        #### final operations    
        self.x=sum(map(lambda x, y: x*y, x_new,W))  
        self.y=sum(map(lambda x, y: x*y, y_new,W))  
        self.col=map(int,((self.col[0]+COL[0])/2,(self.col[1]+COL[1])/2,(self.col[2]+COL[2])/2))
    
        return self
     
    
    #def multiV(self,nm,Ws,As,COLs,fW,sym=True):
    def multiV(self):
        rn=random.rand()
        ## ugly
        i=config.nm
        for t in range(config.nm):
            if rn<config.fW[t]:
                i=t
                break
            
        self.F(config.Ws[i],config.As[i],config.COLs[i])
        
        if(config.sym==True):
            rnbis=random.rand()
            if(rnbis<.5):
                self.x=-self.x
                self.y=-self.y
        
        return self


class Worker(multiprocessing.Process):
    """
    Generic worker class. You can make any worker
    inherit from it and simply create a work method
    where the calculation is performed and returned.
    Then the result can be retrieved by the output property.
    """
    def __init__(self):
        super(Worker, self).__init__()
        self.result = multiprocessing.Queue()

    @property
    def output(self):
        return self.result.get()

    def run(self):
        self.result.put(self.work())

def run_pool(workers, n_jobs=-1, sleep=0.1):
    """
    Helper function to execute a list of processes in //
    """
    # defensive copy
    workers = workers[:]
    if n_jobs < 1:
        n_jobs = multiprocessing.cpu_count()
    processes = []
    p = None
    try:
        while True:
            active = multiprocessing.active_children()
            while len(active) < n_jobs and len(workers) > 0:
                p = workers.pop(0)
                p.start()
                processes.append(p)
                active = multiprocessing.active_children()
            if len(workers) == 0 and len(active) == 0:
                break
            time.sleep(sleep)
    except KeyboardInterrupt, SystemExit:
        if p is not None:
            p.terminate()
        for p in processes:
            p.terminate()
        raise

################

     

class P_Worker(Worker):
    """
    This is probably not the most elegant and the
    most efficient way to code this but it works.
    The worker class has to be instantiated with all the arguments
    Then each argument are passed as class attribute to the work method
    and since you want to get the object back the work method returns it.
    ----
    Now that I think about it, you could simply inherit P_worker from Process
    and put the calculation there. The nice think of the Worker class is that
    it encapsulate all of the multiprocessing things. The P_Worker can only be 
    about what you want to compute.

    """

    def __init__(self,P):#, P,nm,Ws,As,COLs,fW,sym):
        self._P = P
#        self._nm = nm
#        self._Ws=Ws
#        self._As=As
#        self._COLs=COLs
#        self._fW=fW
#        self._sym=sym
        super(P_Worker, self).__init__()

    def work(self):
        #self._P.multiV(self._nm,self._Ws,self._As,self._COLs,self._fW,self._sym)
        self._P.multiV()        
        return self._P


        
        
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
    
    #def mutemV(self,nm,Ws,As,COLs,fW,sym,multi_proc):
    def mutemV(self,multi_proc):
        if multi_proc:
            #workers = [P_Worker(p,nm,Ws,As,COLs,fW,sym) for p in self.bloc]
            workers = [P_Worker(p) for p in self.bloc]
            run_pool(workers, n_jobs=N_JOBS)
            self.bloc = [p.output for p in workers]
        else:   
             for p in self.bloc:
                 #p.multiV(nm,Ws,As,COLs,fW,sym)
                 p.multiV()
     
      
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
            if(xpt_mod < sizeImage and xpt_mod >0 and ypt_mod < sizeImage and ypt_mod>0):
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
    