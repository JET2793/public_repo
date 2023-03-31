#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 01/01 12:00:00 2020

@author: jthompson
"""
import cmath
from lmfit import Model
from lmfit import Parameters
import numpy as np


#Function to find location of closest value to a specified value in an array
def find_nearest_T(value,array):
    return (np.argmin(abs(array-value)))

# Define functions to calculate Ic, Rn
def RSJ_A(r, R, Ic):
    return r*R*cmath.sqrt(1-(Ic/r)**2).real

def RSJ(x,R,Ic):
    b=np.empty(len(x), dtype=float)
    for i in range(len(x)):
        b[i]=RSJ_A(x[i], R, Ic)
    return b

#Initialise Model Class
RSJmodel = Model(RSJ, independent_vars=('x'))

#Initialising first Estimate Parameters
params=Parameters()
params.add('R', value=0.0015,min=0,max=1)
params.add('Ic', value=0.0000075, min=0.00, max=1.0)


# Assign measured data to variable
V1 = np.array("your array of measured voltage", dtype=float)
I1 = np.array("your array of measured current", dtype=float)

#Change these to modify which data points from array are used in modelling (set m=0 and n=1 to model all data)
m=0
n=1
    
#Fitting individual I-V to RSJ model
RSJmodel_result = RSJmodel.fit(V1[m:-n],x=I1[m:-n], params=params, nan_policy='propagate')
    
#Extracting fitted parameters
Rn = RSJmodel_result.params['R'].value
erRn = RSJmodel_result.params['R'].stderr
Ic = RSJmodel_result.params['Ic'].value
erIc = RSJmodel_result.params['Ic'].stderr


#Visualising RSJ fit for datafile modelled
fig0 = RSJmodel_result.plot(show_init=False)
RSJmodel_result.params.pretty_print()


