# -*- coding: utf-8 -*-
"""
The base level Instruction and InstructionTree classes.

Instruction is a node in a tree.  Each Instruction contains forward links 
to subsequent instruction(s).  

The code refereced by Instruction executes and, when it's
finished, the instructions referenced by the forward links are executed
in parallel, thus opening further branches on the tree.
If an Instruction contains no forward links, the branch will terminate.

The InstructionTree is a special Instruction that serves to contain an
internal set of Instructions.  Any forward linked Instruction(s) will not
exectue until all of the internal Instructions complete, effectivley merging
excution branches of the tree back into a single node.  Any of the internal
Instruction in an InstructionTree may itself be an InstructionTree
allowing one to nest complex sets of instructions inside of the tree

The animation sequencer begins at the head of the tree, which is an
InstructionTree instance, and executes the instructions in the order described
by the tree structure.

Created on Fri Sep  6 15:05:28 2019
@author: G. Ruch
"""

class Instruction():
    """A basic node in the Instruction Tree.

    Instruction contains an update function holding the code for the
    instruction as well as links to subsequent instructions.

    Attributes
    ----------
    nextInstructions : list of Instructions
        The instruction(s) to execute when this instruction finishes

    finished : boolean
        True when the instruction has finished executing
    """

    def __init__(self,next_instructions=[]):
        self._next_instructions = []

        # Add next instructions through the interface in case
        # we change the underlying data structure later
        self._next_instructions=[]
        self.add_instructions(next_instructions)

        # Changed attribute.  Set to True for instructions that change a
        # a mobject requiring a re-rendering.  Assuming True by default
        self.frame_changed = True

        self._finished = None

    def add_sequential(self,instructions):
        """Add a set of sequential instructions

        Parameters
        ----------
        instructions : list of Instruction instances
            The list of instructions to add to the tree
        """
        if len(instructions) == 0:
            return

        # Link the instructions
        parent = self
        for inst in instructions:
            parent.add_instructions([inst])
            parent = inst

    def add_instructions(self,instructions):
        """Add an instruction to be executed when the current one finishes.

        If multiple instructions are added they will run in parallel
        """
        self._next_instructions.extend(instructions)

    @property
    def next_instructions(self):
        return self._next_instructions

    def start(self,scene):
        """Execute any additional setup before the first call to update."""
        pass

    def update(self,scene,dt):
        """Move the instruction forward dt seconds

        This is where the code to control the animation goes.
        To build an Instruction, inherit this class and over-ride the update
        method.

        The animation sequencer will call the update method with a reference to
        current Scene and a time increment (dt) representing the time to the
        the next animation frame.

        update must return the amount of time actually used by the instruction,
        has a maximum of dt if the instruction has more work to do or some value
        less than dt if the instruction finished before dt elapsed.

        Parameters
        ----------
        scene : Scene instance
            The scene on which to execute the instruction

        dt : float
            Time to advance the instruction in seconds

        Returns
        -------
        dtUsed : float
            The number of animation seconds that the instruction actually 
            consumed.
            dtUsed will be less than dt if the instruction finished
            during dt elapsed
        """
        raise NotImplementedError("Over-ride me!")

    @property
    def finished(self):
        if type(self) is Instruction:
            raise NotImplementedError("Over-ride me!")
        else:
            return self._finished

    @finished.setter
    def finished(self,val):
        if type(self) is Instruction:
            raise NotImplementedError("Over-ride me!")
        else:
            self._finished = val


    def calcTimeUsed(self,timeLeft,dt):
        if timeLeft > dt:
            return (dt,dt/timeLeft)
        else:
            return (timeLeft,1)

class InstructionTree(Instruction):
    """Execute a set of instructions in the proper sequence.

    Attributes
    ----------
    instructions : List of Instructions
        The instructions to execute
    """

    def __init__(self, initial_sequence=[],
                       next_instructions=[]):
        """Set up

        Parameters
        ----------
        instructions : optional list of instructions
            Instructions to execute before executing the instructions in
            nextInstructions
        """
        super().__init__()

        # Each element represents a chain of sequential instructions
        self._current_instructions = []
        self.add_current_instructions(initial_sequence)
        self.add_sequential(next_instructions)
        self.finished = False

    @property
    def current_instructions(self):
        return self._current_instructions

    def add_current_instructions(self,instructions):
        """Add instructions to execute on the next call to update
        
        Parameters
        ----------
        *instructions : tuple of Instructions
            The set of instructions to execute on the next call to update
        
        """   
        if (len(instructions) > 0):
            self._current_instructions.extend(instructions)

    def start(self,scene):
        """Send start signal to the leading instructions"""
        for inst in self._current_instructions:
                inst.start(scene)

    def update(self,scene,dt):
        """Execute all currently active instructions"""
        dtUsed, self._current_instructions = self._update(
            scene, self._current_instructions, dt)  
        if len(self._current_instructions) == 0:
            self.finished = True
        return dtUsed

    def _update(self,scene,instructions,dt):
        """Internal recursive update function
        # Allow each instruction in instructions to step forward a time dt
        # If an instruction finishes before dt elapses:
        #   1. Remove it from the list
        #   2. recursively call _update with with the unused time and the
        #      nextInstructions list. If no further instructions are pending,
        #      terminate the chain.
        """
        total_run_time = 0.0
        # Fetch the next instruction
        for inst in instructions.copy():

            # run this instruction for dt seconds.
            dt_used = inst.update(scene,dt)

            # Check the instruction to see if it has made changes to the scene
            # If the scene hasn't changed, the renderer doesn't need to render
            if(inst.frame_changed):
                scene.frame_changed = True

            # Did the instruction finish?
            if inst.finished:

                # Instruction terminated, Remove it from the queue
                try:
                    instructions.remove(inst)
                except:
                    import sys
                    e = sys.exc_info()[0]
                    print(e)
                    raise e


                # Get the next set of instructions started
                for i in inst.next_instructions:
                    i.start(scene)

                # Recursively use up any unused time on the next
                # set of instructions
                new_dt_used, new_instructions = self._update(
                    scene, inst.next_instructions, dt-dt_used)

                # update the timer and append any new instructions
                # to our list of currently executing instructions
                dt_used += new_dt_used
                self.add_current_instructions(new_instructions)

            # Update the total time used
            if dt_used > total_run_time:
                total_run_time = dt_used

        return total_run_time, instructions



