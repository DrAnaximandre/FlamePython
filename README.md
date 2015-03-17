# FlamePython
Another implementation of Flames Fracals in Python

All this work comes from the idea of Draves and Recase (http://flam3.com/flame_draves.pdf)

The main idea is to randomly sample a large number of points (500k will do) in the [-1:1] square. Each point is colored, starting as white (RBG [255,255,255]). Then, each point is "attracted" with an attractor function (starting with an injective function). The function modifies the coordinates of the point, but also its colour. The attractor is applied several times to insure an approximated convergence) (10-15 times works fine on Serpiensky's triangle attractor). The result is then a fractal flame.

So far, the "serpiensky_togif.py" file illustrates the convergence of such an algorithm, as it generates a gif file where the first frame is an image of 500k white points randomly disposed in the square, and each following frame is an iteration of the attraction. Frame after frame, the (coloured) Sepriensky's triangle appears. 
NB: for a further work, it is not advised to generate a png image of each step of the convergence, as it is quite long. 



