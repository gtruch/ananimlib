# -*- coding: utf-8 -*-

"""
The core instruction set.

These are the most abstract instructions.
Other more concrete instructions are built from these basic forms.

Created on Sat Dec  7 22:00:16 2019
@author: Fred
"""

import ananimlib as al

import copy as cp


class RunSequential(al.InstructionTree):
    """Chains a tuple of Instrucions to execute sequentially.
    
    Parameters
    ----------
    *instruction : tuple of Instructions
        The instructions to run
    """
    
    def __init__(self, *instructions):
        super().__init__()  
        self.finished = False
        
        # Set the forward links on each instruction
        if(len(instructions) > 1):
            instructions[0].add_sequential(instructions[1:])


        # Put the lead instrucions in the "current" list
        if (len(instructions) > 0):
            self.add_current_instructions(instructions[0:1])
    
        
    
class RunParallel(al.InstructionTree):
    """Sets a tuple of instructions to execute in parallel.
    
    Parameters
    ----------
    *instruction : tuple of Instructions
        The instructions to run
    """
    
    def __init__(self, *instructions):
        super().__init__(instructions)
        self.finished = False
        


class SetAttribute(al.Instruction):
    """Set an attribute of a anobject to the desired value.

    If the attribute is callable, it is called with value as the parameter
    Otherwise, the attribute is set to value

    If value is callable, it is called with the current Timing and its return
    value is used to set the attribute.

    eg. obj.attribute = value
        obj.attribute = value(time,timing)
        obj.attribute(value)
        obj.attribute(value(time,timing))
        
    Parameters
    ----------
    key : string
    attribute : string
    
    value : 
    """

    def __init__(self,key, attribute, value,
                      anobject = None, duration=0.0,
                      transfer_func=al.linear):
        """Set up.

        Parameters
        ----------
        key : str
            The key for the object to update

        attribute : string
            The name of the attribute

        value : type undefined
            if value is callable:
                value = value(scene.time,timing)
                where
                    time is the global animation time before dt.
                    timing is a CoreInstructions.Timing object.

        anobject : optional object
            Provide a direct reference to the anobject instead of a key.
            If anobject is None, key is used to get the anobject from the scene.
            If anobject is not None, key is ignored.
            default = None

        duration : optional, float
            The amount of time in seconds to allow the instruction to execute.
            duration < 0.0 means run indefinitely
            default: 0.0

        """
        self.key = key
        self.attribute = attribute
        self.value = value

        self.timing = Timing(duration,transfer_func=transfer_func)
        self.anobject = anobject
        self.finished = False

        super().__init__()


    def start(self,scene):
        """Animation sequencer calls start before the first call to update."""

        # Get a reference to the object
        if self.anobject is None:
            self.anobject =  scene.get_anobject(self.key)

        if callable(self.anobject):
            self.anobject = self.anobject()

        # Make sure that the requested attribute exists
        if not hasattr(self.anobject,self.attribute):
            raise AttributeError("'%s' object has no attribute '%s'"%(
                            type(self.anobject).__name__,self.attribute))
        else:
            self.attr = getattr(self.anobject,self.attribute)


    def update(self,scene,dt):
        """Update the attribute.

        scene : Scene
            The scene associated with the animation

        dt : float
            The amount of time to move forward during this step
        """

        # Update the timing module
        self.timing.update(dt)

        # Is value callable?
        if callable(self.value):
            value = self.value(scene.time,self.timing)
        else:
            value = self.value

        # is the attribute callable?
        if callable(self.attr):
            if value is None:
                self.attr()
            else:
                self.attr(value)
        else:
            setattr(self.anobject,self.attribute,value)

        if self.timing.time_left == 0:
            self.finished = True

        return self.timing.time_used


class SlideAttribute(SetAttribute):
    """
    Incrementally update a numeric attribute over a fixed period of time.

    The attribute is updated as:
        obj.attribute = (new_value-old_value)*transfer_function(alpha)

        where alpha is the ratio of the current time used by the instruction
        to the requested duration

    Parameters
    ----------
    key : AnObject or string
        The ID of the AnObject to update

    attribute: string
        The name of the attribute

    end_value: type undefined
        The target value of the attribute.

    start_value: optional, type undefined
        The starting value of the attribute.
        If start_value = None, the current value of the attribute is used.
        default = None

    duration: optional, float
        The amount of time in seconds over which to update the attribute.
        default: 0.0

    relative: optional, boolean
        Set to True if the end value should be relative to the current 

    transfer_func: callable
        A function that maps alpha to a new ratio between 0 and 1
        ratio = transfer_func(alpha)
        default = smooth

    anobject : optional AnObject
        Provide a direct reference to the object rather than a key.
        If anobject is None, the key is used to look the object up.
        If anobject is not None, the key is ignored.
        default = None

    """

    # ToDo: Add a relative flag with the following logic: 
    #       start_value = anobject.attribute
    #       if relative is True
    #           end_value   = start_value+end_value
    #       else 
    #           
    
    def __init__(self, key, attribute, end_value, 
                 start_value   = None,
                 duration      = 0.0,
                 relative      = False,
                 transfer_func = al.smooth,                 
                 anobject      = None):

        self.end_value = end_value
        self.start_value = start_value
        self.relative = relative
        super().__init__(key           = key,
                         attribute     = attribute,
                         value         = self._iliketomoveitmoveit,
                         anobject       = anobject,
                         duration      = duration,
                         transfer_func = transfer_func)

    def start(self,scene):
        super().start(scene)

        if self.start_value is None:
            self.start_value = getattr(self.anobject,self.attribute)
            
        if self.relative:
            self.end_value += self.start_value

        # Callable start and end values don't work here...
        if callable(self.end_value):
            self.end_value = self.end_value(0,0)
        if callable(self.start_value):
            self.start_value = self.start_value()

    def _iliketomoveitmoveit(self,time,timing):
        diff = -1*(self.start_value-self.end_value)
        ratio = timing.alpha
        return self.start_value+diff*ratio

    
class Transform(al.Instruction):
    """Smoothly Transform one BezierAnObject into another

    Parameters
    ----------
    key : dict key
        The key for the bezieranobject to transform

    target : BezierAnObject
        The bezieranobject that we wish to become

    duration : float
        The time in seconds for the transformation to occur
    """

    def __init__(self,key,target,duration=0.0):
        self.key=key
        self.target=target
        self.duration=duration
        self.timing = Timing(duration)
        self.finished = False
        super().__init__()

    def start(self,scene):
        """Let's get ready to rumble"""

        # Get a reference to the object
        self.anobject =  scene.get_anobject(self.key)

        # Get the starting path and the target path
        self.start_path = cp.deepcopy(self.anobject.data)
        self.target_path = cp.deepcopy(self.target.data)

        # Split the shorter path until they have the same number of segments


    def update(self,scene,dt):

        # Update the timing module
        self.timing.update(dt)

        if self.timing.time_left == 0:

            # All done, adopt the original target curve
            self.anobject.data.points = self.target_path.points
            self.finished = True

        else:

            # In between.  Interpolate intermediate curves
            sp = self.start_path.points
            tp = self.target_path.points

            self.anobject.data.points = sp + (tp-sp)*self.timing.alpha

        return self.timing.time_used

class Group(al.Instruction):
    """Group a set of anobjects to lock them spatially together.
    """

    def __init__(self,name,anobjects):
        """Group anobjects

        Parameters
        ----------
        name : str
            The name of the group

        anobjects : List of strings
            The names of the anobjects to add to the group
        """

        self.name = name
        self.anobjects = anobjects
        super().__init__()

    def update(self,scene,dt):

        group = al.CompositeAnObject()

        # Add anobjects to a composite and remove from them from the scene
        for mobName in self.anobjects:
            anobject = scene.get_anobject(mobName)
            group.add_anobject(anobject,mobName)
            scene.remove_anobject(mobName)

        # Add the composite to the scene
        scene.add_anobject(self.name,group)
        self.finished=True

        return 0.0

class Timing():
    """Handle timing for instructions

    Attributes
    ----------
    duration : float
        The total amount of time requested

    time_left : float
        The amount of time yet to be used (duration - time_used)

    time_used : float
        The total amount of time used during the current frame

    total_time_used : float
        The total time used for all frames

    alpha : float
        the ratio of total_time_used/duration
        alpha is modified by the chosen transfer function.

    """

    def __init__(self,duration,transfer_func=al.linear):
        """
        Parameters
        ----------
        duration : float
            The amount of time over which to execute the instruction

        transfer_func : optional callable
            A function to modify the alpha parameter
        """

        self.duration = duration
        self._time_used = 0
        self._total_time_used = 0
        self.transfer_func=transfer_func

    @property
    def time_left(self):
        return self.duration - self._total_time_used

    @property
    def time_used(self):
        return self._time_used

    @property
    def total_time_used(self):
        return self._total_time_used

    @property
    def alpha(self):
        if self.duration > 0.0:
            return self.transfer_func(self._total_time_used/self.duration)
        else:
            return 1.0

    def update(self,dt):

        # Handle the timing.
        if self.time_left > dt:

            # More time left than requested increment
            self._total_time_used += dt     # Use up dt seconds
            self._time_used = dt

        else:
            # Requested increment is less than the remaining time
            self._time_used = self.time_left  # Use up the remaining time
            self._total_time_used = self.duration

