#!/usr/bin/python
# coding=utf-8

import math
import matplotlib.pyplot as plt
import numpy as np
#from numpy.linalg import matrix_power
#from numpy import linalg as LA
from pylab import *

import matplotlib
matplotlib.use('TkAgg')

import pylab as PL
import random as RD
import scipy as SP

import copy as cp


########################################################################################################
#####################################    Mathematic Representation     #################################
########################################################################################################


#Common Formulas
h=1 # Number of Predators currently harvesting prey
s=1-h # Fraction of predator population searching for prey
Ts=5 # Time until predator finds patch of prey 
Th=5 # Time until predator returns to searching

#Formulas Single-predator
H=5 #Consuption rate prey/time
H_max=5 #Consuption rate prey/time when s=0 abundant prey
proportion_H_alone = 1/(1+Ts/Th) # H/H_max


#Formulas Social-predators
Tl=5 # Time until prey patch can be exploited
Td=5 # Time until predator reaches another predator
N=5 # Number of predators hunting in the same area
lambda_share=5 # Propensity of sharing information
m=5 # Number of predators moving toward a broadcasted prey patch 
b=5 # Number of predators reached the patch with broadcaster
proportion_H_social = h+b # H/H_max
Wsh=1/Ts # Rate which lone predators find and start consuming prey patch
Wsm=N*lambda_share*s*Wsh # Rate which lone predators get the broadcast
Wmb=1/Td # Rate which lone predators reach the broadcaster

limit=0.3
#np split function
if lambda_share>limit:
    np=N
else:
    np=1+b/h

WL= 1/Tl + Th/np # Rate which a predator is interupted while exploiting patch (depleation or movement of patch)

#Whs=Wms=Wbs=WL => Rate which predators revert to searching alone
Whs = WL
Wms = Whs
Wbs = Wms


########################################################################################################
#####################################    ABM    ########################################################
########################################################################################################

import matplotlib
matplotlib.use('TkAgg')
from pylab import *
import copy as cp


nr = 500. # carrying capacity of rabbits
r_init = 4 # initial rabbit population
mr = 0.03 # magnitude of movement of rabbits

f_init = 2 # initial fox population
mf = 0.05 # magnitude of movement of foxes

cd = 0.02 # radius for collision detection
cdsq = cd ** 2
patch_population_max = 100

patch_population_limit = 85
consumption_rate=5

sharing = False


def distance_between_2_points(x1,y1,x2,y2):
    dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)  
    return dist


class agent:
    pass


def initialize():
    global agents
    agents = []
    #Creating Rabbits
    for i in xrange(r_init):
        ag = agent()
        ag.type = 'r'
        ag.current_state="static"
        ag.patch_population_curr = patch_population_max
        ag.stay=True
        ag.x = random()
        ag.y = random()
        agents.append(ag)

    #Creating Foxes
    for i in xrange(2):
        ag = agent()
        ag.type = 'f'
        ag.current_state="searching"
        ag.stay=False
        ag.broadcast=False
        ag.x = random()
        ag.y = random()
        agents.append(ag)


def observe():
    global agents
    cla()
    rabbits = [ag for ag in agents if ag.type == 'r']
    if len(rabbits) > 0:
        x = [ag.x for ag in rabbits]
        y = [ag.y for ag in rabbits]
        plot(x, y, 'b.')
    foxes = [ag for ag in agents if ag.type == 'f']
    if len(foxes) > 0:
        x = [ag.x for ag in foxes]
        y = [ag.y for ag in foxes]
        plot(x, y, 'ro')
    axis('image')
    axis([0, 1, 0, 1])


def update():
    global agents
    if agents == []:
        return
    
    ag = agents[randint(len(agents))]

    # simulating random movement
    m = mr if ag.type == 'r' else mf

    if sharing:
        broadcasters_list=[]
        for a in agents:
            if a.type=='f' and a.broadcast==True:
                broadcasters_list.append(a)
        

        if ag.type=='f' and ag.current_state=="searching" and not broadcasters_list:
            ag.x += uniform(-m, m)
            ag.y += uniform(-m, m)
            ag.x = 1 if ag.x > 1 else 0 if ag.x < 0 else ag.x
            ag.y = 1 if ag.y > 1 else 0 if ag.y < 0 else ag.y
            # detecting collision
            neighbors = [nb for nb in agents if nb.type != ag.type and (ag.x - nb.x)**2 + (ag.y - nb.y)**2 < cdsq]
            if len(neighbors) > 0: # if there are rabbit nearby
                ag.current_state="consuming_alone"
                ag.broadcast=True

        
        if ag.type=='f' and ag.current_state=="searching" and broadcasters_list:
            #Not all foxes are broadcasting so this fox will move_to_friend
            if len(broadcasters_list)>0 and len(broadcasters_list)<f_init:
                ag.x += broadcasters_list[0].x-ag.x
                ag.y += broadcasters_list[0].y-ag.y
                ag.x = 1 if ag.x > 1 else 0 if ag.x < 0 else ag.x
                ag.y = 1 if ag.y > 1 else 0 if ag.y < 0 else ag.y
                ag.current_state="moving_to_friend"

         
        if ag.type=='f' and ag.current_state=="consuming_alone":
            # detecting collision
            neighbors = [nb for nb in agents if nb.type != ag.type and (ag.x - nb.x)**2 + (ag.y - nb.y)**2 < cdsq]
            if len(neighbors) > 0: # if there are rabbit nearby
                ag.current_state="consuming_alone"
                nb.population=nb.population-consumption_rate
                ag.broadcast=True
            else:
                ag.current_state="searching"
                ag.broadcast=False
                
            
        if ag.type=='f' and ag.current_state=="moving_to_friend":
            # detecting collision
            neighbors = [nb for nb in agents if nb.type != ag.type and (ag.x - nb.x)**2 + (ag.y - nb.y)**2 < cdsq]
            if len(neighbors) > 0 and 0<distance_between_2_points(ag.x,ag.y,broadcasters_list[0].x,broadcasters_list[0].y)<=cd : # if there are rabbit nearby
                ag.current_state="consuming_with_friend"
                ag.broadcast=True


        if ag.type=='f' and ag.current_state=="consuming_with_friend":
            neighbors = [nb for nb in agents if nb.type != ag.type and (ag.x - nb.x)**2 + (ag.y - nb.y)**2 < cdsq]
            if len(neighbors) > 0: # if there are rabbit nearby
                nb.population=nb.population-2*consumption_rate
                ag.broadcast=True
            else:
                ag.current_state="searching"
                ag.broadcast=False



        ########################################################################
        if ag.type=='r' and ag.current_state=="static":
            if ag.patch_population_curr < ag.patch_population_limit:
                ag.current_state="run"
        
    
        if ag.type=='r' and ag.current_state=="run":
            ag.x += uniform(-m, m)
            ag.y += uniform(-m, m)
            ag.x = 1 if ag.x > 1 else 0 if ag.x < 0 else ag.x
            ag.y = 1 if ag.y > 1 else 0 if ag.y < 0 else ag.y
            ag.patch_population_curr=patch_population_max
            ag.current_state="static" 
    
        return
    else:
        if ag.type=='f' and ag.current_state=="searching":
            ag.x += uniform(-m, m)
            ag.y += uniform(-m, m)
            ag.x = 1 if ag.x > 1 else 0 if ag.x < 0 else ag.x
            ag.y = 1 if ag.y > 1 else 0 if ag.y < 0 else ag.y
            # detecting collision
            neighbors = [nb for nb in agents if nb.type != ag.type and (ag.x - nb.x)**2 + (ag.y - nb.y)**2 < cdsq]
            if len(neighbors) > 0: # if there are rabbit nearby
                ag.current_state="consuming_alone"
            
        if ag.type=='f' and ag.current_state=="consuming_alone":
            # detecting collision
            neighbors = [nb for nb in agents if nb.type != ag.type and (ag.x - nb.x)**2 + (ag.y - nb.y)**2 < cdsq]
            if len(neighbors) > 0: # if there are rabbit nearby
                ag.current_state="consuming_alone"
                nb.population=nb.population-consumption_rate
            else:
                ag.current_state="searching"
                #population modification was here!? and not in consuming_alone 
            
        if ag.type=='r' and ag.current_state=="static":
            if ag.patch_population_curr < ag.patch_population_limit:
                ag.current_state="run"
        
    
        if ag.type=='r' and ag.current_state=="run":
            ag.x += uniform(-m, m)
            ag.y += uniform(-m, m)
            ag.x = 1 if ag.x > 1 else 0 if ag.x < 0 else ag.x
            ag.y = 1 if ag.y > 1 else 0 if ag.y < 0 else ag.y
            ag.patch_population_curr=patch_population_max
            ag.current_state="static" 
    
        return




def update_one_unit_time():
    global agents
    t = 0.
    while t < 1.:
        t += 1. / len(agents)
        update()


import pycxsimulator
pycxsimulator.GUI().start(func=[initialize, observe, update_one_unit_time])