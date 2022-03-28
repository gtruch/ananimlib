# -*- coding: utf-8 -*-
"""
Created on Mon Jun 28 11:33:09 2021

@author: gtruch
"""
# START
import ananimlib as al
  
al.Animate(
    al.AddAnObject(al.Rectangle([1,1]), key = "rect"),
    al.MoveTo("rect", [-3,0]),
    al.Move("rect", [6,0], duration=1.0),
    al.Wait(1.0),
)

al.play_movie()
# END





