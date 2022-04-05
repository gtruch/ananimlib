# -*- coding: utf-8 -*-
"""
Created on Sun Aug  8 17:09:43 2021

@author: Fred
"""
from collections import namedtuple
from os import path



import ananimlib as al


base_path = '../'

    
def main():
    
    al.engine.frame_rate = 50
    al.engine.DPI = 50
    al.engine.reset_scene()
    
    assert(al.engine.scene.camera.frame_rate  == 50)
    assert(al.engine.backend.frame_rate == 50)
        
    figures = [
        "quickstart_ex1",
        "quickstart_ex2",
        "quickstart_ex3",
        "quickstart_ex4",
        "quickstart_ex5",
        "quickstart_ex5_1",
        "quickstart_ex6",
        "quickstart_ex6_1",
        "quickstart_ex7",
        "quickstart_ex8"
    ]
#    figures = ["quickstart_ex2"]

    for fig in figures:
        print(f"creating {fig}")
        
        # Clear out old data
        al.engine.reset_scene()
        
        
        # Rewire al.play_movie to execute save_gif
        al.play_movie = lambda : al.engine.backend.save_gif(
                                           path.join(base_path,fig+".gif"))

        # Execute the code in the file
        with open(fig+".py") as f:
            exec(f.read())
        
    
if __name__=="__main__":
    main()
    

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