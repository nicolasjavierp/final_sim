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


n = 1000 # number of agents
class agent:
    pass

def initialize():
    global agents
    agents = []
    for i in xrange(n):
        ag = agent()
        ag.type = randint(2)
        ag.x = random()
        ag.y = random()
        agents.append(ag)



def observe():
    global agents
    cla() #Clear the graph
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




nr = 500. # carrying capacity of rabbits
mr = 0.03 # magnitude of movement of rabbits
#dr = 1.0 # death rate of rabbits when it faces foxes
#rr = 0.1 # reproduction rate of rabbits
mf = 0.05 # magnitude of movement of foxes
#df = 0.1 # death rate of foxes when there is no food
#rf = 0.5 # reproduction rate of foxes
cd = 0.02 # radius for collision detection
cdsq = cd ** 2
broadcast = True


def update():
    global agents
    if agents == []:
        return
    ag = agents[randint(len(agents))]
    # simulating random movement
    if ag.type == 'r': #and not stay:
        m = mr
    if ag.type == 'f': #and not consuming
        m = mf
    ag.x += uniform(-m, m)
    ag.y += uniform(-m, m)
    ag.x = 1 if ag.x > 1 else 0 if ag.x < 0 else ag.x
    ag.y = 1 if ag.y > 1 else 0 if ag.y < 0 else ag.y

    # detecting collision 
    neighbors = [nb for nb in agents if nb.type != ag.type and (ag.x - nb.x)**2 + (ag.y - nb.y)**2 < cdsq]

    if ag.type == 'r': #if Agent is rabbit
        if len(neighbors) > 0: # if there are foxes nearby
            #Relocate 
            #ag.stay = False
            return

    else: #if Agent is fox
        if len(neighbors) == 0: # if there are no rabbits nearby
            #Initiate Random Search 
            return
        else: # if there are rabbits nearby
            if broadcast:
                #Fox initiates Broadcast
                #Teleport closest Fox/s
                #Fox/s initiate consuption => Num_times_Foxs_ate = Num_times_Foxs_ate + 1
                #ag.consume=True
                return
            else:
                #Fox/s initiate consuption => Num_times_Foxs_ate = Num_times_Foxs_ate + 1
                return
                




import pycxsimulator
pycxsimulator.GUI().start(func=[initialize, observe, update])
