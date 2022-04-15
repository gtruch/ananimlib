# -*- coding: utf-8 -*-
"""
Created on Sun Aug  8 17:10:18 2021
Generate all figures for the Quickstart chapter

@author: G. Ruch

"""
from collections import namedtuple
from os import path

import ananimlib as al


base_path = '../'

    
def main():
    
    # Manually fiddle with the engine's camera settings
    al.engine.frame_rate = 50
    al.engine.DPI = 50

    # Becase we changed the frame size by altering the DPI, we have to call
    # AnEngine.reset() to propagate the changes.  
    # reset also discards any existing frames.
    al.engine.reset_scene()     
    
    # ToDo: Move these two lines into tests
    #       Checking to make sure the above lines work as intended.
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
    
