# -*- coding: utf-8 -*-
"""
A short tutorial about ManimLib2 coordinate systems.

Created on Thu Aug 20 09:14:51 2020

@author: G. Ruch
"""

import manimlib2.Manim             as Manim    # The main animation engine
import manimlib2.CommonMobs        as cmob     # A set of common Mobjects
import manimlib2.Mobject           as mob
import manimlib2.PlotMobs          as pmob     # Mobjects useful for plots
import manimlib2.BasicInstructions as i        # A set of basic instructions
import manimlib2.CoreInstructions  as ci
import manimlib2.TexMobject        as tmob
import manimlib2.Render            as rnd
import numpy as np

import matplotlib.pyplot           as plt

def main():
    r = np.linspace(0,2)
    y = 1/(r**2+1)
    
    plt.figure(1)
    plt.plot(r,y,'.')

def main2():
    
    # Create an instance of the animation engine
    m = Manim.iManim("spinny_coord",backend="pygame")
    
    
    container = mob.CompositeMobject()
    circ = cmob.Rectangle([1.0,1.0])
    arrow = cmob.Arrow([0,0], [2,3])
    container.add_mobject(circ,'circ')
    container.add_mobject(arrow,'arrow')
    
    m.run(
        i.AddMobject('c', container),
        m.runParallel(
            i.Rotate('c', 2*np.pi,duration=1.0),
            ci.AdjustAttribute(['c','arrow'], 'magnitude', 1.0,duration=1.0)
        ),
        i.Wait(1.0)
    )
    
    m.play_movie()

    
def main2():

    # Create an instance of the animation engine
    m = Manim.iManim("spinny_coord",backend="pygame")
    
    about = [-1.5,-1.0]
    position= [5,1]
    rotation = np.pi/6

    # Configure the camera

    # **************************
    # The default coordinate system has the origin centered in the camera
    # window with x values increasing to the left and y values increasing
    # upwards
    # **************************
    m.config_camera(width       = 16,       # Scene Width in inches
                    ar          = 16.0/9.0, # Aspect Ratio width/height
                    frame_rate  = 120,       # Frame rate in Frames per second
                    DPI         = 60)       # Pixel Density in Dots per Inch


    # Create a coordinate grid to overlay in the camera window
    grid = pmob.CoordGrid(
        screen_size   = [16.0, 10.0],  # Size of grid on screen
        grid_size     = [16.0, 10.0],  # Native grid size
        major_spacing = [1.0, 1.0],   # Major ticks
        minor_spacing = [0.2, 0.2])   # Minor ticks
    
    
    
    dot = cmob.Circle(0.05,pen=rnd.Pen(fill_color="#48a4cd",
                                               fill_opacity=1.0,))    
    
    mob2 = mob.CompositeMobject()
    mob2.add_mobject(cmob.Rectangle([4,4],pen=rnd.Pen(fill_opacity=1.0,
                                                      fill_color="#000000")))

    grid2 = pmob.CoordGrid([4,4],[4,4],[1.0,1.0],[0.2,0.2])
    grid2.opacity = 0.5

    mob2.add_mobject(grid2)
    mob2.add_mobject(dot)
    dot.position = about
    about_arrow = cmob.Arrow([0,0], about)
    mob2.add_mobject(about_arrow)

    # Create the About Point label
    ab_text = tmob.Text("\\textit{About Point}", 
                         pen=rnd.Pen(fill_color="#48a4cd",
                                     fill_opacity=1.0,))    
    
    mob2.add_mobject(ab_text)
    ab_text.scale = 0.4
    ab_text.about_upper()
    ab_text.position = [-0.75,-0.7]
    ab_text.rotation_angle = about_arrow.rotation_angle + np.pi

    rect = cmob.Rectangle([1,1])
    mob2.add_mobject(rect)

    mob2.about_point = about
    mob2.position = position
    mob2.scale=0.75
    mob2.rotation_angle = rotation 
    

    pos_arrow = cmob.Arrow([0,0],position)

    # Create the Position label
    pos_text = tmob.Text("\\textit{Position}", 
                     pen=rnd.Pen(fill_color="#48a4cd",
                                     fill_opacity=1.0,))    
    pos_text.about_lower()
    pos_text.position = [2.5,0.6]
    pos_text.scale=0.75
    pos_text.rotation_angle = pos_arrow.rotation_angle

    

    m.run(
        i.AddMobject('grid', grid),
        i.AddMobject('mob2',mob2),
        i.AddMobject('pos_arrow', pos_arrow),
        i.AddMobject('pos_text', pos_text),
        
        i.Rotate('mob2',rotation+2*np.pi,duration=2.0),



        i.Wait(1.0)
    )
    m.play_movie()



if __name__=="__main__":
    main()







