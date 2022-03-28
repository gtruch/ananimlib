#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 28 16:30:43 2021

@author: gtruch
"""

import numpy as np

def linear(t):
    return t

def smooth(t, inflection=6.0):
    error = sigmoid(-inflection / 2)
    return np.clip(
        (sigmoid(inflection * (t - 0.5)) - error) / (1 - 2 * error),
        0, 1,
    )

def sigmoid(x):
    return 1.0 / (1 + np.exp(-x))

def there_and_back(t):
    return 0.5*(1+np.sin(t*2*np.pi-np.pi/2))
