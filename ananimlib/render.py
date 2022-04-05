# -*- coding: utf-8 -*-
"""
Rendering classes

Created on Fri Dec 20 12:34:18 2019

@author: GtRuch
"""
import cairo
import numpy     as np
import ananimlib as al
import colour    as cl

class Render():
    """Render class to pair with the data classes.

    Intended as an Abstract Base Class to define the Render interface

    """

    def render(self,mobject,canvas):
        """Render the data onto the canvas.

        Parameters
        ----------
        data
            A reperesentation of the data for render to access

        canvas
            The canvas on which to render the data

        transform_matrix : ndarray of floats
            A nxn matrix representing an affine transformation of the data
            to be applied prior to rendering
        """
        raise NotImplementedError("Render.render must be implemented " +
                                  "by the subclass")


class CairoRender(Render):
    """Abstract base class for Cairo Render."""

    def __init__(self):

        # When render is called, we need parent_render to run first
        # subsequently call the child class render
        self.child_render = self.render
        self.render = self.parent_render



    def parent_render(self,mobject,camera):
        """Universal Cairo rendering

        Handle matrix manipulations
        Set the clip region
        call the child render
        """


        # Be a good citizen and save the existing context state
        camera.context.save()


        # Set up the new transform matrix
        cmat = camera.context.get_matrix()
        transform_matrix = mobject.transform_matrix
        my_mat = cairo.Matrix(
            transform_matrix[0,0],-transform_matrix[0,1],
            -transform_matrix[1,0],transform_matrix[1,1],
            transform_matrix[0,2],transform_matrix[1,2]
        )

        # Apply the transform matrix to the cairo context
        camera.context.set_matrix(my_mat.multiply(cmat))

        # Apply the clip region if the mobject has one.
        if mobject.clip is not None:
            self.set_path(mobject.clip,camera.context)
            camera.context.clip()

        # Call the child class render
        self.child_render(mobject,camera)

        # Restore the original context
        camera.context.restore()

    def render(self,data,camera):
        """Render the data on the cairo context contained in camera"""

        raise NotImplementedError(
            "render must be implemented in children of CairoRender")

    def set_path(self, path, context):
        """Draw the path described by the bezier curve into the context

        Parameters
        ----------
        path : PolyBezier
            The path to set.

        context : Cairo Context
            The context on which to set the path
        """

        context.new_path()

        # Draw each curve in the path
        p3 = None       # Keep track of endpoints while setting the path
        p0 = None
        for segment in path:
            s_p0 = segment._coefficients[0]
            s_p1 = segment._coefficients[1]
            s_p2 = segment._coefficients[2]
            s_p3 = segment._coefficients[3]

            if p3 is not None:
                diff = p3-s_p0

            # New path if ending point of the previous segment does
            # not match the beginning of current segment
            if p3 is None or np.sqrt(diff[0]**2+diff[1]**2+diff[2]**2) > 1e-9:

                # Save the starting point and begin the new path
                p0 = s_p0
                context.move_to(s_p0[0],s_p0[1])

            # Draw the curve
            context.curve_to(s_p1[0], s_p1[1],
                             s_p2[0], s_p2[1],
                             s_p3[0], s_p3[1])
            # save the end point
            p3 = s_p3


class ImageRender(CairoRender):

    def render(self, mobject, camera):
        """Render the image into the camera frame"""

        ctx = camera.context

        # Render the image onto the base surface
        ctx.set_source_surface(mobject.data.surface,0,0)
        ctx.mask_surface(mobject.data.surface,0,0)


class CompositeRender(CairoRender):
    """Render a group of mobjects

    Position and rotation information are set in the tranform matrix
    before each call to the render for the individual mobjects.
    """

    def render(self,anobject,camera):

        # Render each anobject in the composite. 
        for key in anobject.keys:
            anobject.anobjects[key].render(camera)


class BezierRender(CairoRender):
    """Render Bezier curves into a pyCairo context.

    Attributes
    ----------
    pen : Pen

    """

    def __init__(self,pen=None):

        if pen is None:
            self._pen = Pen()
        else:
            self._pen = pen

        # one line_width is 1/1000th of a frame height
        self.lines_per_frame = 1000.0
        self._partial_path = None

        super().__init__()

    @property
    def pen(self):
        return self._pen

    @pen.setter
    def pen(self,val):
        self._pen = val


    def render(self,mobject,camera):
        """Render the vmobject into the camera's cairo context
        """

        _, frame_height = camera.sceneUnitsPerFrame

        # Create the path described by the bezier curves
        self.set_path(mobject.data,camera.context)

        # Perform the fill and stroke
        self.fill_and_stroke(camera.context,frame_height)



    def fill_and_stroke(self, context, frame_height):
        """Apply the fill and stroke to the path."""


        # Fill
        if self.pen.fill_opacity > 0:
            
            if self.pen.fill_pattern is not None:
                surf = cairo.ImageSurface.create_from_png(self.pen.fill_pattern)            
                pat = cairo.SurfacePattern(surf)                
                context.set_source(pat)
            else: 
            
                # Set source color for fill
                context.set_source_rgba(self.pen.fill_color.red,
                                        self.pen.fill_color.green,
                                        self.pen.fill_color.blue,
                                        self.pen.fill_opacity)
            context.fill_preserve()


        if self.pen.stroke_opacity > 0:

            # We do not want to draw with an elliptical pen.
            # If the x scale is different from the y scale,
            # change it for the stroke and then change it backcbvcnngf clD
            cmat = context.get_matrix()
            if np.abs(cmat.xx) != np.abs(cmat.yy):
                context.save()
                cmat.xx=np.abs(cmat.yy)*np.sign(cmat.xx)
                context.set_matrix(cmat)
                restore_mat = True
            else:
                restore_mat = False

            # Adjust the line width based on the frame size.
            context.set_line_width(
                self.pen.stroke_width*frame_height/self.lines_per_frame)
            context.set_source_rgba(self.pen.stroke_color.red,
                                    self.pen.stroke_color.green,
                                    self.pen.stroke_color.blue,
                                    self.pen.stroke_opacity)
            context.stroke_preserve()

            if restore_mat:
                context.restore()

class Pen():
    """A container for holding stroke and fill parameters for sVMobjects

    Attributes
    ----------
    stroke_color : Color
        The color of the stroke 
    
    stroke_opacity : float
        The opacity of the stroke
    
    stroke_width : float
        The width of the stroke
    
    fill_color : Color
        The fill color
    
    fill_opacity : float
        The fill opacity
    """

    def __init__(self, stroke_color="#FFFFFF",
                       stroke_opacity=1.0,
                       stroke_width=1.0,
                       fill_color="#FFFFFF",
                       fill_opacity=0.0,
                       fill_pattern=None):

        if al._default_pen is None:
            self.stroke_color    = stroke_color
            self.stroke_opacity  = stroke_opacity
            self.stroke_width    = stroke_width
            self.fill_color      = fill_color
            self.fill_opacity    = fill_opacity
            self.fill_pattern    = fill_pattern
        else : 
            self.stroke_color    = al._default_pen.stroke_color
            self.stroke_opacity  = al._default_pen.stroke_opacity
            self.stroke_width    = al._default_pen.stroke_width
            self.fill_color      = al._default_pen.fill_color
            self.fill_opacity    = al._default_pen.fill_opacity
            self.fill_pattern    = al._default_pen.fill_pattern

    @property
    def stroke_color(self):
        return self._stroke_color

    @stroke_color.setter
    def stroke_color(self,color):
        self._stroke_color = cl.Color(color)

    @property
    def fill_color(self):
        return self._fill_color

    @fill_color.setter
    def fill_color(self,color):
        self._fill_color = cl.Color(color)

    # def set_full_render(self):
    #     """Render the full curve on the next call to Render."""
    #     self.set_partial_render(tstart=0.0,tend=1.0)

    # def set_partial_render(self,tend,tstart=0.0):
    #     """Render the portion of the curve between tstart and tend

    #     Subsequent calls to render after a call to renderPartial
    #     will display the desired portion of the path.  Any calls to position,
    #     rotation, etc will be with respect to a bounding box around the full
    #     path.

    #     To restore the full path, call renderPartial with
    #     tstart = 0.0 and tend=1.0

    #     Parameters
    #     ----------
    #     tend : float
    #         The ending position of the partial path where 0<=tend<=1.0

    #     tstart : optional float
    #         The starting position of the partial path where 0.0<=tstart<=1.0
    #     """

    #     # Check parameters
    #     if (tend < 0.0 or tend > 1.0 or
    #         tstart < 0.0 or tstart > 1.0 or tend < tstart):

    #         raise ValueError("tstart and tend must be within 0.0 to 1.0 and " +
    #                          "tend must be greater than tstart.")

    #     # Restore full path?
    #     if tstart == 0.0 and tend == 1.0:
    #         self._partialPath = None
    #     else:

    #         # Split the original path using PolyBezier.split
    #         if tstart > 0.0:
    #             # Take the portion of the original path after tstart
    #             _ , self._partialPath = self.path.split(tstart)
    #         else:
    #             self._partialPath = self.path

    #         # Take the portion of the current partial path before tend
    #         self._partialPath, _ = self._partialPath.split(
    #                                                 (tend-tstart)/(1-tstart))
