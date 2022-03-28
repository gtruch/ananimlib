# -*- coding: utf-8 -*-
"""
Created on Mon May  3 09:35:25 2021

@author: Fred
"""

import manimlib2.Manim             as Manim
import manimlib2.Mobject           as mob
import manimlib2.CommonMobs        as cmob
import manimlib2.TexMobject        as tmob
import manimlib2.BasicInstructions as i

def main():
    
    m = Manim.iManim()
    
    m.config_camera(width       = 16.0, 
                    ar          = 16.0/9.0, 
                    frame_rate  = 60, 
                    DPI         = 100)
    
    rect1 = cmob.Rectangle([3,1])
    text1 = tmob.Text("Instruction 1")
    text1.scale = 0.5
    
    m.run(
        i.AddMobject('rect1', rect1),
        i.AddMobject('text1', text1),
        i.Wait(1.0)
    )

    m.play_movie()
    



if __name__ == "__main__":
    main()