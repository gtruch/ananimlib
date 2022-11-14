# -*- coding: utf-8 -*-
"""
Created on Sun Aug  8 17:10:18 2021
Generate all figures for the Quickstart chapter

@author: G. Ruch

"""
import os
import sys
import math

import ananimlib as al
    
def main():
    
    print(os.getcwd())
    
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
    
    print(f"creating {sys.argv[2]}")
    
    # Clear out old data
    al.engine.reset_scene()
    
    # Rewire al.play_movie to execute save_gif
    al.play_movie = lambda : al.engine.backend.save_gif(sys.argv[2])

    # Execute the code in the file
    with open(sys.argv[1]) as f:
        stuff = f.read()
        exec(stuff,globals())
    
if __name__=="__main__":
    main()
    
