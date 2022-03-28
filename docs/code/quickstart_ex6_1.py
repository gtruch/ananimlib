# -*- coding: utf-8 -*-
"""
Created on Tue Aug 17 11:18:52 2021

@author: Fred
"""
import ananimlib as al


grid = al.CoordGrid([16,10], [16,10], [1,1],[.5,.5])
rect = al.CompositeAnObject()
about = al.Dot()
arrow = al.Arrow([0,0], [0,0])
rect.add_anobject(al.Rectangle([1,1]))
rect.add_anobject(about)

al.Animate(
    al.AddAnObject(grid),
    al.AddAnObject(rect),
    
    al.MoveTo(rect, [3,2],duration=1.0),
            
    al.SetAboutPoint(rect, [-2,-1]),        
)
rect.add_anobject(arrow),
arrow.position=[0,0]
al.Animate(

    al.RunParallel(
        al.MoveTo([rect,about],[-2,-1],duration=1.0),
        al.SlideAttribute([rect,arrow], 'head_pos', 
                           al.Vector([-2,-1]),duration=1.0)
    ),

    al.MoveTo(rect, [0,0],duration=1.0),
    al.Wait(1.0)
)
        
al.play_movie()
