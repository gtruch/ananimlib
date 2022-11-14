# START
import math
import ananimlib as al

box = al.Rectangle(
    size = [1.0,1.0],        
    pen  = al.Pen(
        stroke_color   = "#FFFFFF",
        stroke_opacity = 1.0,
        stroke_width   = 3.0,
        fill_color     = "#cda448",
        fill_opacity   = 1.0
    )
)

wave_angle=60*math.pi/180
    
al.Animate(
    al.AddAnObject(box),
    al.Rotate(box,   wave_angle/2, duration=0.25), 
    al.Rotate(box,  -wave_angle, duration=0.5), 
    al.Rotate(box,   wave_angle/2, duration=0.25),
    al.Wait(1.0)
)

al.play_movie()
# END