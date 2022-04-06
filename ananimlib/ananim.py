# -*- coding: utf-8 -*-
"""
Created on Sat Aug 24 21:42:30 2019

@author: gtruch
"""
import ananimlib as al
import numpy as np

class AnEngine():
    """The central animation engine

    Contains and manages the central animation loop in the *run* method.  
    
    Maintains a references to the *Scene* (the set of AnObjects currently being 
    animated), the *Camera* (generates image frames the *Scene*),  minimal backend that 
    
    
    """

    def __init__(self):

        # Write down some critical parameters
        self.width       = al._defaults['width']
        self.ar          = al._defaults['ar']
        self.frame_rate  = al._defaults['frame_rate']
        self.DPI         = al._defaults['DPI']

        self._render=True

        # reset_scene rebuilds the camra, the backend, and the scene
        self.reset_scene()

        # Render frames by default (Rather than just executing the instructions)
        self.render=True

    def run(self, *instructions):
        """Execute the instructions and render the results

        This is where the main animation loop lives

        Parameters
        ----------
        *instructions :tuple of Instruction
            The set of instructions to run. 
            
        """
        instruction_tree = al.RunSequential(*instructions)
        frame_rate = self.scene.camera.frame_rate
        pw,ph = self.scene.camera.pixelsPerFrame


        dt  = 1.0/frame_rate
        self.backend.start()               # Tell the backend to get ready
        instruction_tree.start(self.scene)  # Tell the instruction tree to get 
                                           # ready

        # Perform a dt=0 update of the scene to execute leading
        # instructions that use no animation time prior to the first render
        instruction_tree.update(self.scene,0.0)

        ###########################
        # The main animation loop #
        ###########################
        while not instruction_tree.finished:

            if self.render:
                # Render the scene
                self.scene.render()

                # Feed the rendered frame into the backend
                self.backend.addFrame(self.scene.frame)

            # Update the scene for the next frame
            instruction_tree.update(self.scene,dt)

        # Tell the Backend that no more frames are coming
        if self.render:
            self.backend.end()
        return self
            
    @property
    def render(self):
        """True when rendering frames"""
        return self._render

    @render.setter
    def render(self,value):
        """True when rendering frames

        Setting render to False causes the animation sequencer to rapidly
        execute instructions and update the scene without rendering frames.

        Useful for testing and debugging long animation sequences.
        """
        if value:
            self._render = True
            self.config_camera(self.width,self.ar,self.frame_rate,self.DPI)
        else:
            self._render = False
            self.config_camera(self.width,self.ar,1,self.DPI)

    @property
    def animation_name(self):
        """The name of the animation"""
        return self.backend_ob.outName

    @animation_name.setter
    def animation_name(self,name):
        """The name of the animation"""
        self._animation_name = name
        self.backend_ob.outName = name

    @property
    def video_directory(self):
        """The location of the output video file"""
        return self.backend_ob.outDir

    @video_directory.setter
    def video_directory(self,directory):
        """The location of the output video file"""
        self.backend_ob.outDir = directory

    def config_camera(self,width, ar, frame_rate, DPI):
        """Reconfigure the video settings.

        Parameters
        ----------
        width : float
            The width of the camera frame in Scene Units

        ar  : float
            The aspect ratio of a frame width/height

        frame_rate : int
            The frame rate in frames per second

        DPI : int
            Dots per Inch. But really, Pixels per Scene Unit
        """

        if self.render:
            self.width      = width
            self.ar         = ar
            self.frame_rate = frame_rate
            self.DPI        = DPI

        # Calculate height based on width and aspect ratio
        height = width/ar

        # Set up the camera
        pixel_height = DPI*height
        pixel_width  = DPI*width
        frame_height = height
        frame_width  = width
        frame_rate   = frame_rate

        # MP4 backend requires an even number of pixels
        if pixel_height%2 > 0:
            pixel_height+=1
        if pixel_width%2 > 0:
           pixel_width+=1

        self.scene.camera = al.Camera(pixel_width,pixel_height,
                                       frame_height,frame_rate,
                                       frame_width)

        # We also need to change the backend
        if self.render:
            self.backend.frameSize  = np.array([pixel_width,pixel_height],
                                               dtype=int)
            self.backend.frame_rate = frame_rate

    def config_backend(self,pw,ph,frame_rate):
        """Set up the backend so that it can receive frames

        Parameters
        ----------
        pw, ph : int
            Dimensions of the frames in pixels

        frame_rate : float
            The frame rate in frames per second
        """
        self.backend = al.Backend(pw,ph,frame_rate)


    def reset_scene(self):
        self.scene = al.Scene(None)
        self.config_backend(self.width*self.DPI, self.width/self.ar*self.DPI,
                            self.frame_rate)
        self.config_camera(self.width,self.ar,self.frame_rate,self.DPI)

    def play_movie(self, repeat=-1):
        """Have the current backend play the movie"""
        self.backend.play_movie(repeat)
