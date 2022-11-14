# START
import math
import ananimlib as al

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

down_arrow = al.Arrow(tail_pos  = [0,-0.5],
                        head_pos  = [0,-1.5],
                        head_size = 0.75,
                        pen       = al.Pen(stroke_width=2.0))
    
up_arrow = al.Arrow(tail_pos    = [0,0.5],
                    head_pos    = [0,1.5],
                    head_size   = 0.75,
                    pen = al.Pen(stroke_width=2.0))


wave_angle=60*math.pi/180
    

al.Animate(
    al.AddAnObject(box),
    al.AddAnObject(down_arrow),
    al.AddAnObject(up_arrow),
    al.RunParallel(
        al.RunSequential(
            al.Rotate(box,   wave_angle/2, duration=0.25), 
            al.Rotate(box,  -wave_angle, duration=0.5), 
            al.Rotate(box,   wave_angle/2, duration=0.25),
        ),
        al.RunSequential(
            al.Rotate(up_arrow,   wave_angle/2, duration=0.25), 
            al.Rotate(up_arrow,  -wave_angle, duration=0.5), 
            al.Rotate(up_arrow,   wave_angle/2, duration=0.25),
        )            
    ),
    al.Wait(1.0)
)

al.play_movie()
# END