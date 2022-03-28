# -*- coding: utf-8 -*-
"""
Basic manimlib2 usage

@author: G.Ruch - 8/3/2020
"""

# Import manimlib2 components
import manimlib2.Manim             as Manim    # The main animation engine
import manimlib2.CommonMobs        as cmob     # A set of common Mobjects
import manimlib2.BasicInstructions as i        # A set of basic instructions

import numpy as np


def main ():

    # Camera Settings - Defines the size and frame rate of the animation
    DPI        = 80          # Pixel Density in Dots per Inch
    width      = 16          # Scene Width in inches
    ar         = 16.0/9.0    # Aspect Ratio width/height
    frame_rate = 60          # Frame rate in Frames per second

    # Create an instance of the animation engine
    # backend keyword option can be either "mp4" or "pygame"
    # by default, video files go to .\video\ManimOut.mp4
    # Output file name is taken from Manim.animation_name
    m = Manim.iManim(backend="pygame")

    # Configure the camera
    m.config_camera(width, ar, frame_rate, DPI)

    # Instantiate some mobjects to animate
    rect = cmob.Rectangle([4,4])
    circle = cmob.Circle(2)
    arrow = cmob.Arrow(tail_pos=[0,0], head_pos=[2,0])

    # Give the animation engine a list of instructions to execute
    m.run(

        # Add the mobjects to the scene
        i.AddMobject('rect',rect),
        i.AddMobject('circle',circle),
        i.AddMobject('arrow',arrow),

        # Wait for one second
        i.Wait(1.0),

        # Move the circle to a new location and then back
        i.MoveTo('circle', [2,2],duration=1.0),
        i.Wait(1.0),
        i.MoveTo('circle', [0,0],duration=1.0),

        # Rotate the square
        i.Rotate('rect', np.pi,duration=1.0),
        i.Wait(1.0),

        # Spin the arrow around once
        i.Rotate('arrow',2*np.pi,duration=1.0),
        i.Wait(1.0),

        # Simultaneously spin the arrow and move both the arrow and the circle
        m.runParallel(
            i.MoveTo('circle',[3,-2],duration=1.0),
            i.MoveTo('arrow', [3,-2],duration=1.0),
            i.Rotate('arrow',4*np.pi,duration=1.0)
        ),

        # Move them back
        m.runParallel(
            i.MoveTo('circle',[0,0],duration=1.0),
            i.MoveTo('arrow', [0,0],duration=1.0),
            i.Rotate('arrow',0,duration=1.0)
        ),
        i.Wait(1.0)
    )

    # Play the rendered animation
    m.play_movie()



if __name__=="__main__":
    main()