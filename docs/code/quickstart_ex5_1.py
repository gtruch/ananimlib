# -*- coding: utf-8 -*-
"""
Created on Tue Aug 17 11:15:17 2021

@author: Fred
"""
# START
import ananimlib as al

a = al.AnEngine()

rect = al.Rectangle([1,1])

al.Animate(
    al.AddAnObject(rect),
    al.MoveTo(rect,[3,2],duration=1.0),        
    al.Wait(1.0),

    al.SetAboutPoint(rect, [-2,-1]),
    
    al.MoveTo(rect,[0,0],duration=1.0),
    al.Wait(1.0)
)
        
al.play_movie()
# END