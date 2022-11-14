# START
import math
import ananimlib as al
import tutorial_snip5 as ts5

def tutorial_snip6():
    
    wave_angle=60                   # Wave angle in degrees
    wave_angle *=  math.pi/180      # Convert to radians

    box = ts5.SlideyBox()
    box.position=[2,0]

    al.Animate(
        al.AddAnObject(box),
        al.RunParallel(
            ts5.wave_attr(box, 'slope', math.pi/4,duration=2.0),
            al.RunSequential(
                al.Move(box, [-4,  0],duration=1.0),
                al.Move(box, [ 4,  0],duration=1.0)
            )
        )
    )

    al.play_movie()

if __name__=="__main__":
    tutorial_snip6()

# END
