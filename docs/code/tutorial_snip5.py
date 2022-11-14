# START

import math
import ananimlib as al
import math as math

def tutorial_snip5():
    
    wave_angle=60                   # Wave angle in degrees
    wave_angle *= 3.1415/180      # Convert to radians

    box = SlideyBox()

    al.Animate(
        al.AddAnObject(box),
        wave_attr(box, 'slope', math.pi/4,duration=1.0),
    )
    
    al.play_movie()
   

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

# Run the animation
if __name__=="__main__":
    tutorial_snip5()
else:
    print(__name__)

# END
