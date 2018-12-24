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

r_init = 4 # initial rabbit population
mr = 0.03 # magnitude of movement of rabbits

f_init = 2 # initial fox population
mf = 0.05 # magnitude of movement of foxes

cd = 0.02 # radius for collision detection
cdsq = cd ** 2
patch_population_max = 100

patch_population_limit = 65
consumption_rate=1
steps=0
steps_report=100
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
    for i in xrange(f_init):
        ag = agent()
        ag.type = 'f'
        ag.current_state="searching"
        ag.stay=False
        ag.broadcast=False
        ag.x = random()
        ag.y = random()
        ag.searching=0
        ag.eating=0
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
    global steps, steps_report
    steps=steps+1

    # report eating efficiency
    eating=0
    if steps%steps_report==0:
        print "Pasos: ", steps
        for a in agents:
            if a.type=='f':
                print 1.0*a.eating/steps # for each fox
                eating=eating+a.eating
        print 1.0*eating/steps # for all foxes

    ag = agents[randint(len(agents))]

    # simulating random movement
    m = mr if ag.type == 'r' else mf

    if sharing:
        if ag.type=='f' and ag.current_state=="searching":
            # movement
            ag.x += uniform(-m, m)
            ag.y += uniform(-m, m)
            ag.x = 1 if ag.x > 1 else 0 if ag.x < 0 else ag.x
            ag.y = 1 if ag.y > 1 else 0 if ag.y < 0 else ag.y
            # detecting collision
            neighbors = [nb for nb in agents if nb.type != ag.type and (ag.x - nb.x)**2 + (ag.y - nb.y)**2 < cdsq]
            if len(neighbors) > 0: # if there are rabbits nearby
                ag.broadcast=True
                ag.current_state="consuming_alone"
            else: # did someone find prey?
                ag.broadcast=False
                for a in agents:
                    if a.type=="f" and a.broadcast:
                        ag.current_state="moving_to_friend"
                        break
                    else:
                        ag.current_state="searching"
            ag.searching=ag.searching+1
         
        if ag.type=='f' and ag.current_state=="consuming_alone":
            # no movement
            # detecting collision
            neighbors = [nb for nb in agents if nb.type != ag.type and (ag.x - nb.x)**2 + (ag.y - nb.y)**2 < cdsq]
            if len(neighbors) > 0: # if there are rabbits nearby
                ag.broadcast=True
                ag.current_state="consuming_alone"
                # consume from first patch
                nb= neighbors[0] 
                nb.patch_population_curr=nb.patch_population_curr-consumption_rate
                ag.eating=ag.eating+1
            else:
                ag.broadcast=False
                ag.current_state="searching"
                ag.searching=ag.searching+1
            
        if ag.type=='f' and ag.current_state=="moving_to_friend":
            #Moving to friend
            for a in agents:
                if a.type=="f":
                    if a.broadcast:
                        distancia=distance_between_2_points(a.x,a.y,ag.x,ag.y)
                        ag.x+=(a.x-ag.x)*m/distancia
                        ag.y+=(a.y-ag.y)*m/distancia
                        ag.current_state="moving_to_friend"
                        break
                    else:
                        ag.x += uniform(-m, m)
                        ag.y += uniform(-m, m)
                        ag.x = 1 if ag.x > 1 else 0 if ag.x < 0 else ag.x
                        ag.y = 1 if ag.y > 1 else 0 if ag.y < 0 else ag.y
                        ag.current_state="searching"
            # detecting collision
            neighbors = [nb for nb in agents if nb.type != ag.type and (ag.x - nb.x)**2 + (ag.y - nb.y)**2 < cdsq]
            # we assume we got to the same patch as the predator that broadcasted
            if len(neighbors) > 0:
                ag.current_state="consuming_with_friend"
            else:
                ag.current_state="moving_to_friend"
            ag.searching=ag.searching+1

        if ag.type=='f' and ag.current_state=="consuming_with_friend":
            #No movement
            neighbors = [nb for nb in agents if nb.type != ag.type and (ag.x - nb.x)**2 + (ag.y - nb.y)**2 < cdsq]
            if len(neighbors) > 0: # if there are rabbits nearby
                # consumimos del primer parche en la lista
                nb=neighbors[0]
                nb.patch_population_curr=nb.patch_population_curr-consumption_rate
                ag.broadcast=True
                ag.current_state="consuming_with_friend"
                ag.eating=ag.eating+1
            else:
                ag.current_state="searching"
                ag.broadcast=False
                ag.searching=ag.searching+1

        if ag.type=='r' and ag.current_state=="static":
            if ag.patch_population_curr < patch_population_limit:
                ag.current_state="run"
        
        if ag.type=='r' and ag.current_state=="run":
            ag.x = random()
            ag.y = random()

            #ag.x += uniform(-m, m)
            #ag.y += uniform(-m, m)
            #ag.x = 1 if ag.x > 1 else 0 if ag.x < 0 else ag.x
            #ag.y = 1 if ag.y > 1 else 0 if ag.y < 0 else ag.y
            
            ag.patch_population_curr=patch_population_max
            ag.current_state="static" 
    
        return
    else: # not sharing information
        if ag.type=='f' and ag.current_state=="searching":
            # esto mueve en un CUADRADO de m*m, no en un CIRCULO
            ag.x += uniform(-m, m)
            ag.y += uniform(-m, m)
            # esto limita a 1 valores mayores a 1 y a 0 valores menores a 0 (NO CICLICO)
            ag.x = 1 if ag.x > 1 else 0 if ag.x < 0 else ag.x
            ag.y = 1 if ag.y > 1 else 0 if ag.y < 0 else ag.y
            # detecting collision
            neighbors = [nb for nb in agents if nb.type != ag.type and (ag.x - nb.x)**2 + (ag.y - nb.y)**2 < cdsq]
            if len(neighbors) > 0: # if there are rabbit nearby
                ag.current_state="consuming_alone"
            ag.searching=ag.searching+1
            
        if ag.type=='f' and ag.current_state=="consuming_alone":
            # detecting collision
            neighbors = [nb for nb in agents if nb.type != ag.type and (ag.x - nb.x)**2 + (ag.y - nb.y)**2 < cdsq]
            if len(neighbors) > 0: # if there are rabbit nearby
                nb = neighbors[0]
                ag.current_state="consuming_alone"
                nb.patch_population_curr=nb.patch_population_curr-consumption_rate
                ag.eating=ag.eating+1
            else:
                ag.current_state="searching"
                ag.searching=ag.searching+1
            
        if ag.type=='r' and ag.current_state=="static":
            if ag.patch_population_curr < patch_population_limit:
                ag.current_state="run"
        
    
        if ag.type=='r' and ag.current_state=="run":
            ag.x = random()
            ag.y = random()

            #ag.x += uniform(-m, m)
            #ag.y += uniform(-m, m)
            #ag.x = 1 if ag.x > 1 else 0 if ag.x < 0 else ag.x
            #ag.y = 1 if ag.y > 1 else 0 if ag.y < 0 else ag.y
            
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