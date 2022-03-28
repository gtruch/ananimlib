# -*- coding: utf-8 -*-
"""
Created on Mon Aug 16 10:15:54 2021

@author: Fred
"""
# START
import ananimlib as al

rect = al.Rectangle([1,1])

al.Animate(
    al.AddAnObject(rect),
    
    al.Rotate(rect, 3.14, duration=1.0),
    al.Rotate(rect,    0, duration=1.0),
    al.Wait(1.0),

    al.SetAboutPoint(rect, [-2,-1]),
    
    al.Rotate(rect, 3.14, duration=1.0),
    al.Rotate(rect,    0, duration=1.0),

    al.Wait(1.0)
)

al.play_movie()
# END
        

