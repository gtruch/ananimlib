# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 09:59:47 2022

@author: Fred
"""


def main():
    plotting_snip4()
    al.play_movie()


def plotting_snip4():

    grid = al.CoordGrid(
        screen_size    = [10.0, 8.0],
        grid_size      = [4.0, 8.0],
        major_spacing  = [ 1.0, 1.0],
        minor_spacing  = [ 0.2, 0.2],
        offset         = [ 0.0, 0,0])

    # The gold colored box
    box = al.Rectangle(
        size = [1.0,2.0],        
        pen  = al.Pen(
            stroke_color   = "#FFFFFF",
            stroke_opacity = 1.0,
            stroke_width   = 2.0,
            fill_color     = "#cda448",
            fill_opacity   = 1.0
        )
    )

    grid.add_anobject(box,update_transform=False)


    al.Animate(
        al.AddAnObject(grid),
        al.Rotate([grid,box],2*np.pi,duration=1.0),
        al.Wait(1.0)
    )


# START3


import numpy     as np
import ananimlib as al

def plotting_snip3():
    
    # Set up the coordinate grid.  
    grid = al.CoordGrid(
        screen_size    = [10.0, 8.0],
        grid_size      = [4.0, 8.0],
        major_spacing  = [ 1.0, 1.0],
        minor_spacing  = [ 0.2, 0.2],
        offset         = [ 0.0, 0,0])
    dot = al.Rectangle([1,1])


    points = [[x,x*x] for x in np.linspace(-2,2)]
    
    
    data = al.BezierAnObject(pen=al.Pen(stroke_width=3.0))
    data.connect_smooth(points)

    grid.add_anobject(data, update_transform=False)
    data.position=[0,0]
        
    grid.add_anobject(dot)

    al.Animate(
        al.AddAnObject(grid),
        al.RunParallel(
            al.FollowPath([grid,dot], data.data, duration=2.0),
#            al.AlignWithPath([grid,dot], path = data.data, duration=2.0),
        ),
        al.Wait(1.0)
    )





# END3

# START2

import math
import ananimlib as al

def plotting_snip2():
    
    # Set up the coordinate grid.  
    grid = al.CoordGrid(
        screen_size    = [10.0, 8.0],
        grid_size      = [10.0, 8.0],
        major_spacing  = [ 1.0, 1.0],
        minor_spacing  = [ 0.2, 0.2],
        offset         = [ 0.0, 0,0])
    
    dot1 = al.Dot()
    dot2 = al.Dot(radius=0.2,pen=al.Pen(fill_color="#80ACAA",
                                        fill_opacity=0.5))
                
    grid.add_anobject(dot1)
    dot1.position = [5,4]
    dot2.position = [5,4]
        
    al.Animate(
        al.AddAnObject(grid),
        al.AddAnObject(dot2),
        al.Wait(1.0),
        al.RunParallel(
            al.Move([grid,dot1],[-10, -8], duration=3.0),
            al.Move(dot2,       [-10, -8], duration=3.0),
            shrinky_spin_move(grid,      duration=2.0),
        ),
        al.Wait(1.0),
        al.RunParallel(
            al.MoveTo([grid,dot1],[0, 0], duration=1.0),
            al.MoveTo(dot2,       [0, 0], duration=1.0),
            al.Scale(grid, 1.0, duration=1.0),
            al.MoveTo(grid,[0,0],duration=1.0)
        ),
        al.Wait(1.0)
    )
    
    

# STOP2


# START1

import math
import ananimlib as al

def plotting_snip1():
    
    

    # Set up the coordinate grid.  
    grid = al.CoordGrid(
        screen_size    = [10.0, 8.0],
        grid_size      = [10.0, 8.0],
        major_spacing  = [ 1.0, 1.0],
        minor_spacing  = [ 0.2, 0.2],
        offset         = [ 0.0, 0,0])
    
    dot = al.Dot()
    
    grid.add_anobject(dot)
    dot.position = [5,4]
    
    
    al.Animate(
        al.AddAnObject(grid),
        al.Wait(1.0),
        al.RunParallel(
            al.Move([grid,dot],[-10, -8], duration=3.0),
            shrinky_spin_move(grid,      duration=2.0),
        ),
        al.Wait(1.0),
        al.MoveTo([grid,dot],[0,0],duration=1.0),
        al.Wait(1.0)
    )
    
    

def shrinky_spin_move(key,duration=1.0):
    return al.RunSequential(
        al.Scale(key, 0.5,duration=duration/2.25),
        al.Wait(duration/2.25*0.25),
        al.RunParallel(
            al.Move(key,[-4.0,1.5],  duration=duration/2.25),
            al.Rotate(key, 2*math.pi,duration=duration/2.25)
        )
    )
        


# STOP1


if __name__=="__main__":
    main()