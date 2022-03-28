# -*- coding: utf-8 -*-
"""
Created on Mon Aug 16 10:25:48 2021

@author: Fred
"""
import ananimlib as al
import numpy as np

grid = al.CoordGrid([16,10], [16,10], [1,1],[.5,.5])
rect = al.CompositeAnObject()
about = al.Dot()
arrow = al.Arrow([0,0], [0,0])
rect.add_anobject(al.Rectangle([1,1]))
rect.add_anobject(about)
#    rect.add_mobject(arrow)

al.Animate(
    al.AddAnObject(grid),
    al.AddAnObject(rect),
    
    al.Rotate(rect, np.pi,duration=1.0),
    al.Rotate(rect, 0,duration=1.0),
            
    al.SetAboutPoint(rect, [-2,-1]),        
)
rect.add_anobject(arrow),
al.Animate(

    al.RunParallel(
        al.MoveTo([rect,about],[-2,-1],duration=1.0),
        al.SlideAttribute([rect,arrow], 'head_pos', 
                           al.Vector([-2,-1]),duration=1.0)
    ),

    al.Rotate(rect, np.pi,duration=1.0),
    al.Rotate(rect, 0,duration=1.0),
    
    
    al.Wait(1.0)
)
    
al.play_movie()