# -*- coding: utf-8 -*-
"""
Created on Sun Aug  8 17:09:43 2021

@author: Fred
"""

import ananimlib as al

def main():
    example1_2()

def example1_1():
    
    a = al.AnEngine()
    
    a.config_camera(width        = 16, 
                    ar           = 16/9, 
                    frame_rate   = 60, 
                    DPI          = 100)

    rect = al.Rectangle([1,1])

    a.run(
        al.AddAnObject(rect),
        al.MoveTo(rect, [-3,0]),
        al.Move(rect, [6,0], duration=1.0),
        al.Wait(1.0),
    )

    a.play_movie()

def example1_2():
    
    a = al.AnEngine()
    
    a.config_camera(width        = 16, 
                    ar           = 16/9, 
                    frame_rate   = 60, 
                    DPI          = 100)

    rect = al.Rectangle([1,1])

    a.run(
        al.AddAnObject(rect),
        al.SetAttribute(rect, "position", [-3,0]),
        al.SlideAttribute(rect, "position", [3,0],duration=1.0),
        al.Wait(1.0),
    )

    a.play_movie()

if __name__=="__main__":
    main()