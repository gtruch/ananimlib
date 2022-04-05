 # -*- coding: utf-8 -*-
"""
A set of basic instructions.

Created on Sat Dec  7 22:53:04 2019
@author: Fred
"""

import ananimlib as al
import numpy     as np
import copy      as cp

class AddAnObject(al.Instruction):
    """Add a anobject to the scene.

    Parameters
    ----------
    anobject : AnObject
        An instance of a class derived from AnObject

    key : dictionary key
        Key used to reference the AnObject

    """

    def __init__(self,anobject,key=None):

        self.anobject=anobject
        self.key = key
        self.finished = False
        super().__init__()

    def update(self,scene,dt):
        """Add the anobject."""

        if callable(self.anobject):
            self.anobject=self.anobject()

        scene.add_anobject(self.anobject,self.key)
        self.finished = True

        # This operation uses no time
        return 0.0

class RemoveAnObject(al.Instruction):
    """Remove AnObject from the scene.

    Parameters
    ----------
    key : dict key
        The name of the anobject to remove
    """

    def __init__(self,key):
        self.key = key
        self.finished = False
        super().__init__()

    def update(self,scene,dt):
        """Remove the anobject."""
        scene.remove_anobject(self.key)
        self.finished = True

        # This operation uses no time
        return 0.0

class Wait(al.Instruction):
    """Pause execution of the animation branch.

    Parameters
    ----------
    time : float
        Time in seconds to pause the animation branch
    """

    def __init__(self,time):
        super().__init__()

        self.timing = al.Timing(time)
        self.finished = False
        self.frame_changed = False


    def update(self,scene,dt):
        """Don't do anything.  Just sit here."""
        self.timing.update(dt)

        if self.timing.time_left == 0:
            self.finished = True

        return self.timing.time_used

class MoveTo(al.SlideAttribute):
    """Absolute Move of a anobject to a new spot in the Scene.

    Parameters
    ----------
    key: dict key
        The name o

    position: Vector
        The new coordinates of the anobject in Scene Units

    duration: optional float
        The amount of time over which to move the anobject.
        default = 0.0, instantaneous

    transfer_func: optional callable
        The transfer function mapping alpha to the fraction of the total
        distance moved 
        default = smooth
        
    """

    def __init__(self, key, position, duration=0.0,
                      transfer_func=al.smooth):
        super().__init__(key        = key,
                          attribute  = 'position',
                          end_value  = position,
                          duration   = duration,
                          transfer_func = transfer_func)

    def start(self,scene):
        super().start(scene)
        self.end_value=al.Vector(self.end_value)



class Move(al.SlideAttribute):
    """Move the object the desired amount relative its current position

    Parameters
    ----------
    key: dict key
        The name of the anobject to move

    displacement: Vector
        The new coordinates of the anobject in Scene Units

    duration: optional float
        The amount of time over which to move the anobject.
        default = 0.0, instantaneous

    transfer_func: optional callable
        The transfer function mapping alpha to the fraction of the total
        distance moved
        ratio = transfer_func(alpha)
        default = smooth

    """

    def __init__(self, key, displacement, duration=0.0,
                      transfer_func=al.smooth):
        super().__init__(key        = key,
                          attribute  = 'position',
                          end_value  = displacement,
                          duration   = duration,
                          transfer_func = transfer_func)

    def start(self,scene):
        super().start(scene)
        self.end_value=al.Vector(self.end_value)
        self.end_value=self.end_value+self.anobject.position


class Rotate(al.SlideAttribute):
    """Absolute rotation of a anobject wrt its default orientation.

    Parameters
    ----------
    key : dict key
        The name of the anobject to be moved

    angle : float
        The new rotation angle in radians

    duration : optional float
        The amount of time over which to rotate the anobject.
        default = 0.0, instantaneous
    """

    def __init__(self,key,angle,duration=0.0,
                 transfer_func=al.smooth):
        super().__init__(key        = key,
                         attribute  = 'rotation_angle',
                         end_value  = angle,
                         duration   = duration,
                         transfer_func = transfer_func)


class Scale(al.SlideAttribute):
    """Scale a anobject.

    Parameters
    ----------
    key : dict key
        Name of the anobject to scale

    xscale : float
        x-axis scale factor

    yscale : optional float
        y-axis scale factor
        if yscale is none, scale the same as x
        default = None

    duration : optional float
        Duration over which to scale the anobject
    """

    def __init__(self,key,xscale,yscale=None,duration=0.0,
                 transfer_func=al.linear):
        if yscale is None:
            yscale = xscale
        super().__init__(key        = key,
                         attribute  = 'scale',
                         end_value  = al.Vector([xscale,yscale,1.0]),
                         duration   = duration,
                         transfer_func = transfer_func)


class AboutCenter(al.SetAttribute):
    """Set the about point to the center of the bounding box

    Parameters
    ----------
    key : dict key
        Name of the anobject to scale

    """
    def __init__(self,key):
        self.frame_changed = False
        super().__init__(key=key,attribute='about_center',value=None)

class AboutLeft(al.SetAttribute):
    """Move x coord of the about point to the left side of the bounding box

    Parameters
    ----------
    key : dict key
        Name of the anobject to scale

    """
    def __init__(self,key):
        self.frame_changed = False
        super().__init__(key=key,attribute='about_left',value=None)

class AboutRight(al.SetAttribute):
    """Move x coord of the about point to the right side of the bounding box

    Parameters
    ----------
    key : dict key
        Name of the anobject to scale

    """
    def __init__(self,key):
        self.frame_changed = False
        super().__init__(key=key,attribute='about_right',value=None)

class AboutUpper(al.SetAttribute):
    """Move y coord of the about point to the top of the bounding box

    Parameters
    ----------
    key : dict key
        Name of the anobject to scale

    """
    def __init__(self,key):
        self.frame_changed = False
        super().__init__(key=key,attribute='about_upper',value=None)

class AboutLower(al.SetAttribute):
    """Move y coord of the about point to the bottom of the bounding box

    Parameters
    ----------
    key : dict key
        Name of the anobject to scale

    """
    def __init__(self,key):
        self.frame_changed = False
        super().__init__(key=key,attribute='about_lower',value=None)


class AdjustAboutPoint(al.SetAttribute):
    """Adjust the about point relative to its current location

    Parameters
    ----------
    key : dict key
        Name of the anobject to scale

    offset : Vector
        The offset to apply to the current about_point
    """
    def __init__(self,key,value):
        self.frame_changed = False
        super().__init__(key=key,attribute="about_point",value=value)

    def start(self,scene):
        """Calculate the new value of the about_point"""
        super().start(scene)
        self.value = self.anobject.about_point + al.Vector(self.value)


class SetAboutPoint(al.SetAttribute):
    """Set the about point of a anobject

    Parameters
    ----------
    key : dict key
        Name of the anobject to scale

    about_point : Vector
        The new coordinates of the about_point
    """
    def __init__(self,key,about_point):
        self.frame_changed = False
        super().__init__(key,attribute="about_point",value=about_point)

class Draw(al.Instruction):
    """Animate the drawing of a BezierAnObject

    Parameters
    ----------
    key : string
        The key to the BezierAnObject in the scene

    duration : float
        The time to finish drawing
    """

    def __init__(self,key,duration=0.0):
        self.key    = key
        self.timing = al.Timing(duration)
        self.finished = False
        super().__init__()


    def start(self,scene):
        """Save the original data object from the anobject"""
        self.anobject = scene.get_anobject(self.key)
        self.original_data = self.anobject.data


    def update(self,scene,dt):
        """Replace the data object with a partially drawn data object"""

        self.timing.update(dt)      # Update the timer

        if self.timing.time_left > 0:
            # Split the bezier curve at the point indicated by timing.alpha
            # (or split any object that has implemented the split method)
            t = self.original_data.D(self.timing.alpha)
            left,_ = self.original_data.split(self.timing.alpha)

            self.anobject.data = left
        else:

            # Total time has elapsed.  Restore the original curve
            self.anobject.data = self.original_data
            self.finished = True

        return self.timing.time_used


class MoveCamera(al.SlideAttribute):
    """Move the camera within the scene

    Parameters
    ----------
    position : array_like, float
        The position of the center of the camera frame in Scene Units

    duration : float
        The amount of time over which to move the camera.
        default = 0.0, instantaneous
    """

    def __init__(self,position,duration=0.0):
        super().__init__(key           = '__camera__',
                         attribute     = 'position',
                         end_value  = np.array(position),                         
                         duration      = duration,
                         transfer_func = al.smooth)


class ZoomCamera(al.SlideAttribute):

    """Zoom camera in or out about the center of the frame

    The Zoom level is absolute and tied to Scene Units
    Zoom = 1   means that there is 1 Scene Unit per camera frame
    Zoom = 0.5 means that there are 0.5 Scene Units per camera frame

    Parameters
    ----------
    yzoom : float
        The zoom value for the y-axis

    duration : float
        The amount of time over which to execute the zoom.
        default = 0.0, instantaneous

    xzoom : optional float
        The zoom value fo the x-axis.
        If xzoom is None, it is scaled to preserve the aspect ratio
        default = None
    """

    def __init__(self,yzoom,duration=0.0,xzoom=None):
                    
        super().__init__(
                  key           = '__camera__',
                  attribute     = 'sceneUnitsPerFrame',
                  end_value     = [xzoom,yzoom],
                  duration      = duration,
                  transfer_func = al.smooth)
        
    def start(self,scene):
        """Over ride start to fix the aspect ratio."""
        
        # If x-zoom isn't specified, scale it to preserve the aspect ratio
        cur_zoom = scene.camera.sceneUnitsPerFrame
        if self.end_value[0] is None:
            self.end_value[0] = cur_zoom[0]/cur_zoom[1]*self.end_value[1]
                
        super().start(scene)



class Emphasize(al.SlideAttribute):
    """Change the scale of a anobject and then return it to its original size

    Parameters
    ----------
    key : dict key

    scale_mult : optional float
        The multiplier to apply to the original scale.
        default = 2.0

    duration : float
        Number of seconds that the animation should last.
    """
    def __init__(self, key, scale_mult = 2.0, duration=0.0):
        self.scale_mult = scale_mult

        super().__init__(key        = key,
                         attribute  = 'scale',
                         end_value  = 0.0,
                         duration   = duration,
                         transfer_func=al.there_and_back)

    def start(self,scene):
        super().start(scene)
        self.end_value = self.anobject.scale*self.scale_mult



class FollowPath(al.SetAttribute):
    """Have a anobject follow a pre-defined path

    Parameters
    ----------
    key : dict key
        The anobject to move along the path

    path : PolyBezier
        A PolyBezier curve defining the path

    end_points : iterable
        The starting and ending point on the Bezier curve

    duration : float
        The number of seconds the trip should take
    """
    def __init__(self,key,path,duration,end_points=None,transfer_func=al.linear):
        self.key      = key
        self.path     = path
        self.duration = duration
        if end_points is None:
            self.end_points = [0.0,1.0]
        else:
            self.end_points = end_points

        super().__init__(key=key,
                         attribute = 'position',
                         value = self.value_func,
                         transfer_func=transfer_func,
                         duration=duration)

    def value_func(self,time,timing):
        tseg = (timing.alpha*(self.end_points[1]-self.end_points[0])
                                                     +self.end_points[0])
        return self.path.D(tseg)

class AlignWithPath(al.SetAttribute):
    """Align a anobject's rotation angle with slope of path.

    Parameters
    ----------
    key : dict key
        The anobject to adjust

    path : PolyBezier
        A PolyBezier curve defining the path

    start_point : optional, float 0.0<=start_point<=1.0
        The starting point along the path
        default = 0.0

    end_point : optional, float
        The ending point along the path
        default = start_point

    duration : optional float
        The number of seconds the trip should take
        default = 0.0
    """
    
    def __init__(self,key,path, end_points, duration=0.1,transfer_func=al.linear):
        self.key      = key
        self.path     = path
        self.duration = duration

        if end_points is None:
            self.end_point = [0.0,1.0]
        else:
            self.end_points = end_points



        super().__init__(key=key,
                         attribute = 'rotation_angle',
                         value = self.value_func,
                         transfer_func=transfer_func,
                         duration=duration)

    def value_func(self,time,timing):


        tseg = (timing.alpha*(self.end_points[1]-self.end_points[0])
                                                     +self.end_points[0])
        slope = self.path.Dprime(tseg)
        theta = al.Vector(slope).theta*180/np.pi
        theta2 = np.arctan2(slope[1],slope[0])*180/np.pi

        return al.Vector(slope).theta

        

class Swap(al.RunParallel):
    """Swap two anobjects
    
    Parameters
    ----------
    anobject1, anobject2 : AnObject
        The objects whose positions will be swapped.
        
    duration : optional float
        The amount of animation time that the swap should take.
        default = 0.0
        
    transfer_func : callable
        
    """
    
    def __init__(self,anobject1,anobject2,
                 duration=0.0, transfer_func=al.smooth):
        super().__init__()
        self.finished = False
        self.anobject1 = anobject1
        self.anobject2 = anobject2
        self.duration = duration
         
    def start(self,scene):
        
        # Fetch the objects so that we can build the MoveTo instructions
        # self.anobject1 = scene[self.anobject1]
        # self.anobject2 = scene[self.anobject2]
        
        # Set MoveTo instructions to execute in paralell
        self.add_current_instructions([
            al.MoveTo(self.anobject1, 
                      scene[self.anobject2].position,
                      duration=self.duration),
            al.MoveTo(self.anobject2, 
                      scene[self.anobject1].position,
                      duration=self.duration)
        ])
        super().start(scene)
        
                
class GrowArrow(al.SlideAttribute):
    """Grow an arrow from zero to full size"""

    def __init__(self,key,duration,transfer_func=al.smooth):
        super().__init__(key = key,
                         attribute='magnitude',
                         end_value=1.0,
                         start_value=0.0,
                         duration=duration,
                         transfer_func=transfer_func)

    def start(self,scene):
        super().start(scene)
        self.end_value=self.anobject.magnitude



class Repeat(al.Instruction):
    """Repeat an instruction a fixed number of times"""

    def __init__(self,instruction,num):
        """Set up

        Parameters
        ----------
        instruction : Instruction
            The instruction to repeat

        num : int
            Number of times to repeat the instruction
        """
        self.instruction = instruction
        self.num = num
        self.finished = False
        self.frame_changed = instruction.frame_changed
        super().__init__()

    def start(self,scene):
        self.current_inst = cp.deepcopy(self.instruction)
        self.current_al.start(scene)
        self.num -= 1

    def update(self,scene,dt):

        time_used = 0
        while not self.current_inst.finished and time_used < dt:
            time_used += self.current_inst.update(scene,dt-time_used)
            if self.current_inst.finished:
                if self.num > 0:
                    self.start(scene)
                else:
                    self.finished = True
        return time_used


class AddAnObjects(al.Instruction):
    """Add an AnObject to the scene.

    Parameters
    ----------
    keys : list of keys
        Keys used to reference the AnObjectss

    anobjects : list of AnObjectss
        A list of objects derived from AnObject
    """

    def __init__(self,keys,anobjects):

        self.anobjects = anobjects
        self.keys = keys
        self.finished = False
        super().__init__()

    def update(self,scene,dt):
        """Add the anobject."""
        for k,m in zip(self.keys,self.anobjects):
            scene.add_anobject(k,m)
        self.finished = True

        # This operation uses no time
        return 0.0


class BringToTop(al.Instruction):
    """Bring an anobject to the top of the z-order

    Parameters
    ----------
    key : dictionary key
        Key used to reference the AnObject

    """

    def __init__(self,key):
        self.key=key
        self.finished=False
        super().__init__()

    def update(self,scene,dt):
        scene.bring_to_top(self.key)
        self.finished = True

        return 0.0

class DrawText(al.InstructionTree):


    def __init__(self,key,duration):
        """Save all of the things"""
        super().__init__()
        self.key = key
        self.duration=duration

    def start(self,scene):
        """Ok, Let's unpack!"""

        mob = scene.get_anobject(self.key)

        # Split the requested draw time equally between each glyph.
        dt = self.duration/len(mob.data.keys())

        if isinstance(self.key,list):
            kkey=cp.copy(self.key)
        else:
            kkey = [self.key]

        seq = []    # Instruction sequence
        pens = []   # Store the original pen.

        # Turn all of the characters off
        for sym in mob.data.keys():

            # Save the orginal Pen
            pens.append(cp.deepcopy(mob.data[sym].renderer.pen))

            seq.append(al.SetAttribute(kkey+[sym],'stroke_opacity',0.0))
            seq.append(al.SetAttribute(kkey+[sym],'fill_opacity',0.0))

        # Draw and fill each character
        for sym,pen in zip(mob.data.keys(),pens):
            seq.append(al.SetAttribute(kkey+[sym],'stroke_opacity',1.0))
            seq.append(Draw(kkey+[sym],duration=dt))
            seq.append(al.SetAttribute(kkey+[sym],'stroke_opacity',
                                        pen.stroke_opacity))
            seq.append(al.SetAttribute(kkey+[sym],'fill_opacity',
                                        pen.fill_opacity))


        self.add_sequential(seq)
        super().start(scene)

