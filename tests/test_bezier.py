#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  1 10:50:22 2021

@author: gtruch
"""

import numpy as np

def test_BezierCurve_T():
    
    import ananimlib.bezier as bz
    
    # Build a bezier curve
    curve = bz.BezierCurve([[0,0,0],[1,2,3],[2,3,4],[3,4,5]])
    
    # Get coordinates along the curve
    u_orig = np.linspace(0,1,num=10)
    p = np.array([curve.B(t) for t in u_orig])
    
    for param in [0,1,2]:

        # Turn the coordinates back into Bezier parameters
        u_recovered = np.array([curve.T(x,param=param) for x in p[:,param]])

        # Check the results
        np.testing.assert_allclose(u_recovered, u_orig,rtol=0,atol=1e-7)

def test_PolyBezier_T_2D():
    
    import ananimlib.bezier as bz
    
    # Build a PolyBezier curve from a set of three points
    curve = bz.PolyBezier()
    curve.connect_smooth([[0,0,0],
                          [1,2,3],
                          [2,3,4]])
    
    
    # Get coordinates along the curve
    u_orig = np.linspace(0,2,num=10)
    p = np.array([curve.B(t) for t in u_orig])
    
    for param in [0,1]:

        # Turn the coordinates back into Bezier parameters
        u_recovered = np.array([curve.T(x,param=param) for x in p[:,param]])

        # Check the results
        np.testing.assert_allclose(u_recovered, u_orig,rtol=0,atol=1e-7)
#test_PolyBezier_T()