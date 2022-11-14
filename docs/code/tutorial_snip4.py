# START

import math
import ananimlib as al

wave_angle=60                   # Wave angle in degrees
wave_angle *=  math.pi/180      # Convert to radians

# Custom instruction to "wave" an AnObject
def wave(key,wave_angle,duration):
    return al.RunSequential(
        al.Rotate(key,  wave_angle/2, duration = duration/4), 
        al.Rotate(key, -wave_angle,   duration = duration/2), 
        al.Rotate(key,  wave_angle/2, duration = duration/4),
    )

# The gold colored box
box = al.Rectangle(
    size = [1.0,1.0],        
    pen  = al.Pen(
        stroke_color   = "#FFFFFF",
        stroke_opacity = 1.0,
        stroke_width   = 2.0,
        fill_color     = "#cda448",
        fill_opacity   = 1.0
    )
)

# The arrows
down_arrow = al.Arrow(tail_pos  = [0,-0.5],
                        head_pos  = [0,-1.5],
                        head_size = 0.75,
                        pen       = al.Pen(stroke_width=2.0))
    
up_arrow = al.Arrow(tail_pos    = [0,0.5],
                    head_pos    = [0,1.5],
                    head_size   = 0.75,
                    pen = al.Pen(stroke_width=2.0))

# Fix the up-arrow about point so that it rotates with the box.
up_arrow.about_point -= [0.5,0.0,0.0]



al.Animate(
    al.AddAnObject(down_arrow),
    al.AddAnObject(up_arrow),
    al.AddAnObject(box),
    al.RunParallel(
        wave(box     , wave_angle, duration = 1.0),
        wave(up_arrow, wave_angle, duration = 1.0)
    ),
    al.Wait(1.0)
)
   
al.play_movie()
# END
