# -*- coding: utf-8 -*-
"""
Created on Sun Apr 10 08:38:48 2022

@author: Fred
"""

from os import path

import ananimlib as al
import tutorial  as tut_module

base_path = '../'

    
def main():
    
    ignore = ['SlideyBox','wave','wave_attr']
    
    # Manually fiddle with the engine's camera settings
    al.engine.frame_rate = 50
    al.engine.DPI = 50

    # Becase we changed the frame size by altering the DPI, we have to call
    # AnEngine.reset() to propagate the changes.  
    # reset also discards any existing frames.
    al.engine.reset_scene()     

    # Get a list of figures from the tutorial module
    figures = dir(tut_module)
    figures = [fig for fig in figures if callable(getattr(tut_module,fig))]
    figures = [fig for fig in figures if fig not in ignore]
 

    # Call each figure generation function 
    # Then, call save_gif using the function name as a base
    for fig in figures:
        al.engine.reset_scene()
        print(type(getattr(tut_module,fig)))
        print(f"Building {fig}.gif")
        getattr(tut_module,fig)()      # Call the function
        al.engine.backend.save_gif(path.join(base_path, fig + '.gif'))


if __name__=="__main__":

    main()        