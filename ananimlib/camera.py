# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 16:03:48 2019

@author: Fred
"""

import ananimlib as al

from PIL import Image
import cairo
import numpy as np

# TODO: Camera should inherit from Mobject for access to the coordinate 
#       transform code.

# TODO: Interface is janky.  Change to width,height,DPI 

# Is the camera a Mobject?  Or should it just have a Coordinate instance.  


class Camera():
    """Holds a single camera frame.

    Contains information to convert from scene coords to pixel coords.
    Contains the current camera frame.
    Offers a cairo context onto which Mobjects can render themselves

    Attributes
    ----------
    frame : hxwx4 ndarray of floats
        The current camera frame represented as an array of RGBA pixels

    pixelsPerFrame : 1x2 ndarray, int
        The number of pixels per camera frame

    sceneUnitsPerFrame : 1x2 ndarray, float
        The number of Scene units in a single camera frame

    cameraPosition : 1x2 ndarray, float
        The position of the center of the camera window in Scene Coordinates

    ctx : cairo.Context
        A Cairo context attached to the frame for rendering
    """

    def __init__(self,  pixel_width,pixel_height,
                 frame_height,frame_rate,
                 frame_width=0.0,
                 camera_x_center=0.0,camera_y_center=0.0,
                 camera_rotation=0.0,**kwargs):
        """
        Parameters
        ----------
        pixel_width, pixel_height : Int
            The height and width of the camera frame in pixels

        frame_width, frame_height  : float
            The number of Scene Units per Camera Frame.
            This effectively changes the "zoom level" of the camera.
            Small values zoom in, Large values zoom out.

        camera_x_center, camera_y_center : float
            The position of the center of the camera frame in Scene coordinates

        frame_rate : int
            The number of camera frames per second for the animation

        camera_rotation : int

        """

        self._cameraPosition     = np.array(
                [camera_x_center, camera_y_center],dtype=float)
        self._pixelsPerFrame     = np.array(
                [pixel_width, pixel_height],dtype=int)
        self._sceneUnitsPerFrame = np.array(
                [frame_width, frame_height],dtype=float)
        self.frame_rate = frame_rate

        if frame_width == 0.0:
            self._fix_aspect_ratio()

        # Initialize the camera frame
        self._create_cairo_context()
        self.clearFrame()

    @property
    def position(self):
        return self._cameraPosition

    @position.setter
    def position(self,newPos):
        self._cameraPosition = np.array(newPos)
        self._setMatrix()

    @property
    def sceneUnitsPerFrame(self):
        if self._sceneUnitsPerFrame[0] is None:
            self._fix_aspect_ratio()
        return self._sceneUnitsPerFrame

    @sceneUnitsPerFrame.setter
    def sceneUnitsPerFrame(self,newVal):
        self._sceneUnitsPerFrame = newVal
        if self._sceneUnitsPerFrame[0] == 0.0:
            self._fix_aspect_ratio()
        self._setMatrix()

    def setSceneHeight(self,frameHeight):
        self.sceneUnitsPerFrame = np.array([0.0,frameHeight])

    @property
    def pixelsPerFrame(self):
        return self._pixelsPerFrame

    @pixelsPerFrame.setter
    def pixelsPerFrame(self,val):
        self._pixelsPerFrame = val

    @property
    def context(self):
        return self._ctx

    def clearFrame(self):
        """Clear the frame to prepare for next image."""
        self._ctx.set_source_rgb(0.0,0.0,0.0)
        self._ctx.paint()

    def render(self,mob):
        mob.render(self)
        
    @property
    def rgba_frame(self):
        """Return current frame in rgba format"""
        
        # Cairo rendered frames are in BGRA order.
        # Swap Red and Blue layers
        f = self.frame.copy()
        f[:,:,2],f[:,:,0] = f[:,:,0],self.frame[:,:,2]
        return f


    def _fix_aspect_ratio(self):
        frameWidth, frameHeight = self._sceneUnitsPerFrame
        if frameWidth == 0.0:
            pw,ph = self.pixelsPerFrame
            frameWidth = frameHeight*pw/ph
            self._sceneUnitsPerFrame = np.array([frameWidth,frameHeight])

    def _create_cairo_context(self):
        """Get a cairo context based on the pixel dimensions and scale."""
        pw,ph = self.pixelsPerFrame

        # Create the frame and the attached cairo context
        self.frame = np.zeros([ph,pw,4],dtype='uint8')
        self.surface = cairo.ImageSurface.create_for_data(
            self.frame,
            cairo.FORMAT_ARGB32,
            pw, ph
        )

        self._ctx = cairo.Context(self.surface)
        self._ctx.set_antialias(cairo.ANTIALIAS_BEST)
        self._setMatrix()


    def _setMatrix(self):
        """Reset the cairo context transformation matrix."""
        # Set up the transformation from
        # Scene Units to frame pixels

        # Fetch dimensions and scale from the camera
        pw,ph = self.pixelsPerFrame
        fw,fh = self.sceneUnitsPerFrame
        fc = self.position

        self._ctx.set_matrix(cairo.Matrix(
            pw/fw, 0,
            0, -ph/fh,
            (pw / 2) - fc[0] * pw/fw,
            (ph / 2) + fc[1] * ph/fh,
        ))

    def show_frame(self):
        """Use PIL to display the current camera frame"""
        Image.fromarray(self.rgba_frame).show()