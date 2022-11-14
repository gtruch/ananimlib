import ananimlib as al

def tutorial_snip1():
        
# START1

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
# END1
    

def tutorial_snip2():
        
# START2

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
# END2


def tutorial_snip3():
    import ananimlib as al
    al.engine.reset_scene()
    
    
        
# START3

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
# END3
   

def tutorial_snip4():
    import ananimlib as al
    al.engine.reset_scene()
    
    
        
# START4

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
   
# END4


# START5
import math
import ananimlib as al

def tutorial_snip5():
    
    wave_angle=60                   # Wave angle in degrees
    wave_angle *=  math.pi/180      # Convert to radians

    box = SlideyBox()

    al.Animate(
        al.AddAnObject(box),
        wave_attr(box, 'slope', math.pi/4,duration=1.0),
    )
   

class SlideyBox(al.CompositeAnObject):
    """Creates a block with a gravitational vector and a normal vector
    """
    
    def __init__(self):
        super().__init__()
        
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
        
        self.add_anobject(down_arrow)
        self.add_anobject(up_arrow,'up_arrow')
        self.add_anobject(box,'box')
        
        self.slope=0
                   
    @property
    def slope(self):
        return self._slope
    
    
    @slope.setter
    def slope(self, new_slope):
        self._slope = new_slope
        
        # Change the rotation angle of the up arrow and the box
        self.get_anobject('box').rotation_angle      = new_slope
        self.get_anobject('up_arrow').rotation_angle = new_slope+math.pi/2
    
    
# Custom instruction to "wave" an attribute
def wave_attr(key, attribute, wave_distance, duration):
    """Waves an attribute back and forth """
    
    return al.RunSequential(
        al.SlideAttribute(key, attribute, wave_distance/2, 
                          duration = duration/4, relative=True), 
        al.SlideAttribute(key, attribute, -wave_distance  , 
                          duration = duration/2, relative=True), 
        al.SlideAttribute(key, attribute, wave_distance/2, 
                          duration = duration/4, relative=True), 
    )

def wave(key,wave_angle,duration):
    return wave_attr(key,'rotation_angle',wave_angle,duration=duration)

# END5



# START6

import math
import ananimlib as al

def tutorial_snip6():
    
    wave_angle=60                   # Wave angle in degrees
    wave_angle *=  math.pi/180      # Convert to radians

    box = SlideyBox()
    box.position=[2,0]


    al.Animate(
        al.AddAnObject(box),
        al.RunParallel(
            wave_attr(box, 'slope', math.pi/4,duration=2.0),
            al.RunSequential(
                al.Move(box, [-4,  0],duration=1.0),
                al.Move(box, [ 4,  0],duration=1.0)
            )
        )
    )

# END6


if __name__=="__main__":
    tutorial_snip6()
    al.play_movie()
    
    
    