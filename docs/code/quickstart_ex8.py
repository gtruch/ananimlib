# -*- coding: utf-8 -*-
"""
Created on Mon Jun 28 11:33:09 2021

@author: gtruch
"""
# START
import ananimlib as al


def double_move(key, pos1, pos2, duration):
    return al.RunSequential(
        al.Move(key, pos1, duration=duration/2),
        al.Move(key, pos2, duration=duration/2)
    )

al.Animate(
    al.AddAnObject(al.Rectangle([1,1]), "rect"),
    al.MoveTo("rect", [-3.0,0.0]),
    al.RunParallel(
        double_move("rect",[3,2],[3,-2],duration=1.0),    
        al.Rotate("rect", 2*3.1415, duration=1.0),
    ),
    al.Wait(1.0),
    double_move("rect",[-3,2],[-3,-2],duration=1.0),
    al.Wait(1.0)
)
        
al.play_movie()
# END
