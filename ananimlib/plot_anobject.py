# -*- coding: utf-8 -*-
"""

Created on Mon Nov 25 12:32:16 2019

@author: GtRuch
"""

import manimlib2.Mobject as mob
import manimlib2.CommonMobs as cMob
import manimlib2.Bezier as bz
import manimlib2.Coordinates as crd
import manimlib2.Render as rnd
import numpy as np

class PlotMobject(mob.CompositeMobject):
    """A thing to make plots with

    Attributes
    ----------
    xRange, yRange : nx2 array of floats
    xScale, yScale : float
    """

    def __init__(self,xRange=crd.Vector(0.0,0.1),
                 yRange=crd.Vector(0.0,0.1),
                 xScale=1.0,yScale=1.0,
                 axis_pen=rnd.Pen(),
                 plot_pen=rnd.Pen()):
        super().__init__()

        self.plot_pen = plot_pen
        self.axis_pen = axis_pen

        # Create the x and y axis
        xAxis = cMob.Arrow(crd.Vector(xRange[0],0),
                           crd.Vector(xRange[1],0),
                           pen=axis_pen)
        xAxis.about_tail()
        xAxis.position = [xRange[0],0]

        yAxis = cMob.Arrow(crd.Vector(0,yRange[0]),
                           crd.Vector(0,yRange[1]),
                           pen=axis_pen)
        yAxis.about_tail()
        yAxis.position = [0,yRange[0]]

        self.add_mobject(xAxis)
        self.add_mobject(yAxis)

        # Create a mobject to hold the curve
        curve = mob.Mobject(bz.PolyBezier( ),
                                 rnd.VRender(pen=plot_pen))

        self.add_mobject(curve,name="curve")

        self._data=[]

    def add_data(self,new_data):
        """Add data to the plot

        Parameters
        ----------
        new_data : nx3 array of floats
            A list of n data points to add to the plot
        """

        if len(new_data.shape) == 1:
            new_data = np.array([new_data])

        self._data = np.append(
                    self._data,
                    np.array(new_data)).reshape(len(self._data)+len(new_data),2)

        if len(self._data) >= 3:
            curve = self.get_mobject("curve")
            curve.data = bz.PolyBezier()
            curve.data.connectSmooth(self._data)

    # def roll_data(self,new_data):
    #     """Append new_data and remove len(new_data) points"""

    #     self._data = np.append(
    #                     self._data[len(new_data):],
    #                     np.array(new_data)
    #                 ).reshape(len(self._data)+1,2)

    def plot_func(self,func,parm):
        """Plot the function.

        Parameters
        ----------
        func  : callable
            A callable that takes a parameter stored as elements of param and
            returns a numerical value

        param : iterable of parameters
            The parameters taken by func
        """

        # Sample the function
        self._data = np.array([parm,[func(x) for x in parm]]).transpose()

        # Connect the points with a PolyBezier
        self.curve.path = bz.PolyBezier()
        self.curve.path.connectSmooth(self._data)








