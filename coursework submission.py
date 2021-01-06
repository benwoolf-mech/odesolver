# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 16:13:35 2020

@author: benwo
"""

import numpy as np
import matplotlib.pyplot as pl 
import matplotlib.animation as animation

#set max wave speed as 400 m/sec
cmax = 400

#setting height and width of 'stadium' as 150x100 m, and also end time
width = 150
height = 100
tend = 0.5

#setting mesh size, and size of grid in x and y
dx = 1
Nx = int(width/dx) + 1
Ny = int(height/dx) + 1

#defining required arrays in x and y, and the meshgrid to define x and y values for each point
x = np.arange(0,width+dx,dx)
y = np.arange(0,height+dx,dx)
Xg, Yg = np.meshgrid(x,y)

#setting time step using cfl condition
dt = dx/(2*cmax)

#initialising array of all time values
Nt = int(tend/dt) + 1

#array of pressure values in space and time
P = np.zeros((Nt, Ny, Nx))

# initialise grid of wave speed for each point
cgrid = np.zeros((Ny,Nx))
cgrid[:,:int(75/dx)] = 343
cgrid[:,int(75/dx):] = 100

#%%

##set velocity of moving point source as 600 m/s in the x-direction
#v = 600
#        
##set initial x coordinate of projectile
#xposition = 0
#yposition = 50

P[0:5,int(50/dx),int(50/dx)] = 200

#%%
#compute wave equation for all points for each time frame
for t in range(0,Nt):
    #calculate new position of projectile
    xposition = xposition + (v*dt)
    
    #comb through all points in x and y that aren't on the boundaries of the grid:
    for j in range(1,Ny-1):
        for i in range(1,Nx-1):
            
#            #if the point is the location of the projectile, apply a disturbance of +200Pa.
#            if j == yposition/dx and i == int(xposition/dx) and xposition/dx < 300:
##                P[t, j, int(xposition/dx)] = 200
#                pass
#            else:
                #calculate constant term in discretised formula using wave speed at that point
            A = ((cgrid[j,i]**2)*(dt**2))/(dx**2)
            
            #apply discretised formula to calculate new pressure at that point
            P[t, j, i] = A * (P[t-1,j+1,i] + P[t-1,j-1,i] + P[t-1,j,i+1] + P[t-1,j,i-1] - 4*P[t-1,j,i]) - P[t-2,j,i] + 2*P[t-1,j,i]  

    #find and print percentage progress
    progress = (100*t)/Nt
    print(str(round(progress,2)) + '% done')       

#indicate that the render has finished
print('Render Complete')

#%%

#section to generate animation of results

fig1 = pl.figure()

images = []

for p in range(Nt):
    
    frame = P[p, :, :]
    
    image = pl.imshow(frame, animated=True, extent=[0,150,0,100])
    images.append([image])

a = animation.ArtistAnimation(fig1, images, interval=20, blit=True)


pl.show()

#%%

#to generate a contour plot of the pressure distribution at a given time where 0 < t < tend
timetoplot = 0.25

pl.contourf(Xg,Yg,P[int(timetoplot/dt),:,:])
pl.colorbar()

#%%
!brew install imagemagick

a.save('C:\Users\benwo\OneDrive - Imperial College London\Computing Coursework\.gif', writer='imagemagick', fps=60)

