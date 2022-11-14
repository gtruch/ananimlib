# START
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
    
al.Animate(
    al.AddAnObject(box),
    al.Wait(1.0)
)

al.play_movie()
# END
