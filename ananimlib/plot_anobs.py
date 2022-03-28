# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 11:00:57 2020

@author: Fred
"""

import ananimlib as al

import numpy as np
import copy as cp

class Plot(al.CompositeAnObject):
    """Plot a function
    
    Parameters
    ----------
    
    size : optional, Vector
        The size of the plot on the canvas.
        default = same size as the plot area
    
    xrange : optional Vector        
        The range of x-values to display
        default = based on the range in the data.
        
    yrange : Vector
        The range of y-values to display
        default = based on the range in the data.
        
    title : str
    xlabel : str
    ylabel : str
        The title and axis labels 
    
    """
    
    def __init__(self,data=None,size=None,
                 xrange=None, yrange=None, 
                 title=None,xlabel=None,ylabel=None,
                 pen=None,):

        super().__init__()
        self.pen=pen
        
                
        plot = al.CoordGrid([10,6], [5,16],[2,5],[.5,1],origin=[-2.5,4])
        
        self.add_anobject(plot,"plot")
        self.new_curve(self.pen)
        
        if title is not None:
            title=al.Text(title)
            self.add_anobject(title)
            title.position = [5.0,2.0]

        if xlabel is not None:
            xlabel = al.Text(xlabel)
            self.add_anobject(xlabel)
            xlabel.position = [5.0,0.3]
            xlabel.scale=0.5

    def new_curve(self, pen=None):
        if pen is not None:
            self.pen = pen
        self.curve = al.BezierAnObject(pen=self.pen)
        self["plot"].add_anobject(self.curve, preserve_transform=False)
        
    def update(self,time,timing):
        
        if timing.total_time_used > 0.02:
            t = np.arange(0,timing.total_time_used,0.01)
            
            points = []
            for t_ in t:
                points.append(self.plot_func(t_))
                
            self.curve.data = al.PolyBezier()
            pts = np.array([t,points]).transpose()
            self.curve.data.connect_linear(pts)


class CoordGrid(al.CompositeAnObject):

    def __init__(self,screen_size,grid_size,
                     major_spacing,
                     minor_spacing=None,
                     offset=None,
                     major_pen=None,
                     minor_pen=None,
                     text_pen=None,
                     axis_pen=None):
        """A coordinate grid for fun and profit.  

        Parameters
        ----------
        screen_size : array of floats
            The on-screen size of the plot area in User Coordinates

        grid_size : array of floats
            The number of major grid units on the coordinate grid

        major_spacing : array of ints
            The spacing between major grid lines

        minor_spacing : array of ints
            The spacing between minor grid lines

        offset : iterable of floats
            The offset of the origin from the center of the grid. 
            default = [0,0], origin at the center.

        """
        super().__init__()

        self.screen_size   = al.Vector(screen_size)
        self.grid_size     = al.Vector(grid_size)
        self.major_spacing = al.Vector(major_spacing)


        if minor_spacing is None:
            self.minor_spacing=self.major_spacing/4
        else:
            self.minor_spacing = al.Vector(minor_spacing)

        self._opacity = 1.0
        self._major_opacity = 0.75
        self._minor_opacity = 0.5

        scale = self.screen_size*self.grid_size**-1.0
        self.scale = scale

        # Make some pens for drawing
        if major_pen is None:
            self.major_pen  = al.Pen(
                stroke_color = "#2842d7",
                stroke_opacity=self._opacity*self._major_opacity)

        if minor_pen is None:
            self.minor_pen = al.Pen(
                stroke_color = "#6dbf82",
                stroke_opacity=self._opacity*self._minor_opacity)
            
        self.text_pen = text_pen
        self.axis_pen = axis_pen
            
        self._offset = al.Vector([0,0,0])
        if offset is None:
            self.offset = al.Vector([0.0,0.0,0.0])
        else:
            self.offset = al.Vector(offset)

        self._build()
        
    @property
    def offset(self):
        return self._offset
    
    @offset.setter
    def offset(self,value):
        self._offset = al.Vector(value)
        self.about_point = -self._offset
        self.position = [0,0]
        self._build()
            
    @property
    def opacity(self):
        return self._opacity

    @opacity.setter
    def opacity(self,value):
        self._opacity=value
        self.get_anobject('major').stroke_opacity   = (self._opacity*
                                                      self._major_opacity)
        self.get_anobject('minor').stroke_opacity   = (self._opacity*
                                                      self._minor_opacity)
        self.get_anobject('outline').stroke_opacity = self._opacity
        self.get_anobject('axis').stroke_opacity    = self._opacity

        for label in self.text_labels:
            self.get_anobject(label).opacity = self._opacity
            
            
    def _build(self):
        
        self.clear()

        outline = al.Rectangle(self.grid_size,pen=self.major_pen)

        # Create the major grid lines 
        major   = al.Grid(self.grid_size,
                            self.major_spacing,
                            offset = self.offset,
                            pen = self.major_pen)

        # Create the minor grid lines 
        minor   = al.Grid(self.grid_size,
                            self.minor_spacing,
                            offset = self.offset,
                            pen = self.minor_pen)


        # Position all of the grid lines and add them to the composite
        outline.about_center()
        outline.about_point = outline.about_point + self.offset
        outline.position = [0,0]

        major.about_center()
        major.about_point = major.about_point + self.offset
        major.position = [0,0]

        minor.about_center()
        minor.about_point = minor.about_point + self.offset
        minor.position = [0,0]

        self.add_anobject(minor,"minor")
        self.add_anobject(major,"major")
        self.add_anobject(outline,"outline")


        min_axis_value = -self.grid_size/2.0-self.offset
        max_axis_value =  self.grid_size/2.0-self.offset


        # Place the coordinate axis
        axis_path = al.PolyBezier()

        # x-axis
        if min_axis_value[1] > 0:
            ypos = 0
        elif max_axis_value[1] < 0: 
            ypos = max_axis_value[1]
        else:
            ypos = 0
        axis_path.connect_linear([[min_axis_value[0],ypos],
                                 [max_axis_value[0],ypos]])

        # y-axis
        if min_axis_value[0] > 0:
            xpos = 0
        elif max_axis_value[0] < 0: 
            xpos = max_axis_value[0]
        else:
            xpos = 0
        axis_path.connect_linear([[xpos,min_axis_value[1]],
                                 [xpos,max_axis_value[1]]])

        axis = al.BezierAnObject(axis_path,pen=self.axis_pen)
        self.add_anobject(axis,"axis")


        # Create x-axis tick labels at the major grid lines. 
        # First major grid line is at zero.
        n_start = np.ceil(min_axis_value[0]/self.major_spacing[0])
        n_stop  = np.floor(max_axis_value[0]/self.major_spacing[0])
        self.text_labels = []
        for num in np.arange(n_start,n_stop)*self.major_spacing[0]:
            if np.round(num,3) <= max_axis_value[0]:
                _num = repr(np.round(num,3))
                text = al.Text(_num,pen=self.text_pen)
                text.position = [num,-0.15+ypos]
                text.scale = [0.3*self.scale[1]/self.scale[0], 0.3]
                self.add_anobject(text)

        # y-axis tick labels
        for num in np.arange(min_axis_value[1],
                              max_axis_value[1]+self.major_spacing[1],
                              step=self.major_spacing[1]):
            if np.round(num,3) <= max_axis_value[1]:
                text = al.Text(repr(round(num,3)),pen=self.text_pen)
                text.about_right()
                text.position = [-0.1+xpos,num]
                text.scale = [0.3*self.scale[1]/self.scale[0],0.3]
                self.add_anobject(text)
                


class CoordAxis(al.CompositeAnObject):
    """A one dimensional coordinate axis with axis labels and tick marks.
    
    Attributes
    ----------
    """

    def __init__(self,screen_size,grid_size,
                 major_spacing=1.0,minor_spacing =0.2,
                 label_offset=-0.2,label_orientation=0.0,origin=0):
        """Get set up.
        
        Parameters
        ----------
        screen_size : array of floats
            The on-screen size of the plot area

        grid_size : array of floats
            The number of major grid units on the grid

        major_spacing : array of ints
            The number of grid units per major tick mark

        minor_spacing : array of ints
            The number of grid units per minor tick mark 

        origin : array of floats
            The position of the origin wrt the center of the grid
            default = 0.0, origin at the center with grid_size/2 grid units
                           in either direction
        """

        super().__init__()

        self._opacity = 1.0
        self._major_opacity = 1.0
        self._minor_opacity = 0.7
        self._label_offset = label_offset
        self._label_orientation = label_orientation
        self._title_offset = -0.7
        self._title_orientation = 0.0
        self.screen_size = screen_size
        self.grid_size = grid_size
        self.major_spacing = major_spacing
        self.minor_spacing = minor_spacing
        self.scale = self.screen_size*self.grid_size**-1.
        self._title = ""
        self._title_mob = None

        self._parts_cache = {}

        self._build_axis()

    def set_vertical_orientation(self):
        self._label_orientation = np.pi*1.5
        self._label_offset = 0.3
        self.rotation_angle = np.pi/2
        self._build_axis()

    def set_horizontal_orientation(self):
        self._label_orientation = 0.0
        self._label_offset = -0.2
        self.rotation_angle = 0.0
        self._build_axis()

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self,new_title):
        self._title = new_title
        self._title_mob = None
        self._build_axis()

    @property
    def title_offset(self):
        return self._title_offset

    @title_offset.setter
    def title_offset(self,new_title_offset):
        self._title_offset = new_title_offset
        self._build_axis()

    @property
    def title_orientation(self):
        return self._title_orientation

    @title_orientation.setter
    def title_orientation(self,new_title_orientation):
        self._title_orientation = new_title_orientation
        self._build_axis()

    @property
    def length(self):
        return self.grid_size

    @length.setter
    def length(self,new_length):
        self.grid_size = new_length
        self.screen_size = new_length*self.scale[0]
        self._build_axis()

    @property
    def label_offset(self):
        return self._label_offset

    @label_offset.setter
    def label_offset(self,offset):
        self._label_offset = offset
        self._build_axis()

    @property
    def label_orientation(self):
        return self._label_orientation

    @label_orientation.setter
    def label_orientation(self,orientation):
        self._label_orientation = orientation
        self._build_axis()


    def _build_axis(self):

        old_coords = cp.deepcopy(self._coordinates)


        self.clear()
        self._coordinates = al.Coordinates()

        self.scale = self.screen_size*self.grid_size**-1.
        self.origin=0
#        self.origin = -self.grid_size/2.0


        # Make some pens for drawing
        major_pen  = al.Pen(stroke_color = "#FFFFFF", # "#d74228",
                             stroke_opacity=self._opacity*self._major_opacity)
        minor_pen = al.Pen(stroke_color = "#FFFFFF", # "#82bf6d",
                            stroke_opacity=self._opacity*self._minor_opacity)


        # Add the axis arrow
        axis_arrow = al.Arrow([0,0],[1,0])
        axis_arrow.magnitude = self.screen_size
        self.add_anobject(axis_arrow)


        # Calculate positions of tick marks
        min_axis_value = -self.grid_size/2.0-self.origin
        max_axis_value =  self.grid_size/2.0-self.origin
        axis_arrow.position = min_axis_value

        min_major = int(min_axis_value/self.major_spacing)*self.major_spacing
        max_major = int(max_axis_value/self.major_spacing)*self.major_spacing
        major_ticks = np.arange(min_major,
                                max_major+self.major_spacing, 
                                self.major_spacing)

        min_minor = int(min_axis_value/self.minor_spacing)*self.minor_spacing
        max_minor = int(max_axis_value/self.minor_spacing)*self.minor_spacing
        minor_ticks = np.arange(min_minor,
                                max_minor+self.minor_spacing, 
                                self.minor_spacing)

        # Remove any major ticks from the minor tick list
        minor_ticks = np.setdiff1d(minor_ticks, major_ticks)

        # Place major tick marks
        maj_tick_path = al.PolyBezier()
        for tick in major_ticks:
            maj_tick_path.connect_linear([[tick *self.scale[0],0.1],
                                         [tick*self.scale[0],-0.1]])
        tick = al.BezierAnObject(path=maj_tick_path,pen=major_pen)
        self.add_anobject(tick)

        # Place minor tick marks
        min_tick_path = al.PolyBezier()
        for tick in minor_ticks:
            min_tick_path.connect_linear([[tick*self.scale[0],0.07],[tick*self.scale[0],-0.07]])
        tick = al.BezierAnObject()(path=min_tick_path,pen=minor_pen)
        self.add_anobject(tick)

        # Create axis labels
        for num in major_ticks:
            _num = repr(np.round(num,3))
            if _num in self._parts_cache:
                text = self._parts_cache[_num]
            else:
                text = al.Text(_num)
            text.position = [num*self.scale[0],self._label_offset]
            text.scale = 0.3
            text.rotation_angle = self._label_orientation
            self.add_anobject(text)

        # Add the axis title
        if self._title_mob is None:
            self._title_mob = al.Text(self._title)
        self._title_mob.scale = 0.4
        self._title_mob.about_center()
        self._title_mob.rotation_angle = self._title_orientation
        self._title_mob.position = [self.grid_size/2*self.scale[0
                                                     ],self._title_offset]
        self.add_anobject(self._title_mob)


        self._coordinates =  old_coords


class PlotPoints(al.CompositeAnObject):
    """Stores a set of individual PlotMarks to manipulate on a graph"""

    def __init__(self,points,radius=0.1):
        """
        Parameters
        ----------
        points : nx2 array of points
            The intial positions of the points to plot

        radius : default float
            Size of the points

        """
        super().__init__()
        self.radius = radius
        self.pen = al.Pen(fill_color = "#fff476",fill_opacity=1.0)
        self.points = points

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self,points):
        self._points = np.array(points)
        self.clear()
        for p in self._points:
            mark = PlotMark(self.radius,dot_pen=self.pen)
            mark.position = p
            self.add_anobject(mark)

    def add_point(self,point):
        """Append a point to the collection"""
        pass

    def about_stored_point(self,index):
        """Move the about point to one of the stored points

        Parameters
        ----------
        index : int
            The index of the desired point

        """
        self.about_point = self._points[index]

    def get_point(self,index):
        return self._points[index]

class PlotMark(al.CompositeAnObject):
    """A dot with marker lines for marking plots-

    Attributes
    ----------
    dot_radius : float
    dot_pen, xpen, ypen : Pen
    xlength, ylength : float
    """

    def __init__(self, dot_radius=1.0, dot_pen=None,
                       xlength=0.0,  xpen=None,
                       ylength=0.0,  ypen=None,
                       xlabel=None, xl_offset=0.0,
                       ylabel=None, yl_offset=0.0,
                       position = None):

        super().__init__()

        # Set up the pens
        if dot_pen is None:
            self.dot_pen = al.Pen(stroke_opacity=0.0,fill_opacity=1.0)
        else:
            self.dot_pen = dot_pen

        if xpen is None:
            self.xpen = al.Pen()
        else:
            self.xpen = xpen

        if ypen is None:
            self.ypen = al.Pen()
        else:
            self.ypen = ypen

        self.xlength = xlength
        self.ylength = ylength
        self.xl_offset=xl_offset
        self.yl_offset=yl_offset

        self._opacity=1.0
        self._xline_opacity = self.xpen.stroke_opacity
        self._yline_opacity = self.ypen.stroke_opacity
        self._dot_stroke_opacity = self.dot_pen.stroke_opacity
        self._dot_fill_opacity = self.dot_pen.fill_opacity
        self._dot_opacity = 1.0

        if xlabel is None:
            self._xlabel_opacity= 0.0
        else:
            self._xlabel_opacity= 1.0

        if ylabel is None:
            self._ylabel_opacity= 0.0
        else:
            self._ylabel_opacity= 1.0


        # Set up the position
        if position is None:
            position = al.Vector([0,0])
        else:
            position = al.Vector(position)

        # Set up the dot
        self.dot = al.Circle(0.1,pen=self.dot_pen)

        # Set up the x and y lines
        path = al.PolyBezier()
        path.connect_linear([[-position.x,0],[0,0]])
        self.xline = al.BezierAnObject(path)

        path = al.PolyBezier()
        path.connect_linear([[0,-position.y],[0,0]])
        self.yline = al.BezierAnObject(path)

        self.add_anobject(self.xline,'xline')
        self.add_anobject(self.yline,'yline')
        self.add_anobject(self.dot,'dot')

#        self.position = position
        if xlabel is not None:
            self.xlabel_mob = al.TexMath(xlabel)
        else:
            self.xlabel_mob = al.TexMath("x")
        self.add_anobject(self.xlabel_mob,'xlabel_mob')


        if ylabel is not None:
            self.ylabel_mob = al.TexMath(ylabel)
        else:
            self.ylabel_mob = al.TexMath("y")

        self.add_anobject(self.ylabel_mob,'ylabel_mob')

        if position is None:
            self.marker_pos = [0,0]
        else:
            self.marker_pos = position

        self.opacity = self._opacity


    @property
    def marker_pos(self):
        return self.position

    @marker_pos.setter
    def marker_pos(self,pos):

        pos = al.Vector(pos)
        path = al.PolyBezier()
        path.connect_linear([[pos.x+self.ylength,0],[0,0]])
        self.yline.data = path
        self.yline.about_right()
        self.yline.position = pos
        self.ylabel_mob.about_center()
        self.ylabel_mob.about_right()
        self.ylabel_mob.position = [-self.yl_offset,pos.y]

        path = al.PolyBezier()
        path.connect_linear([[0,pos.y+self.xlength],[0,0]])
        self.xline.data = path
        self.xline.about_upper()
        self.xline.position = pos
        self.xlabel_mob.about_center()
        self.xlabel_mob.about_upper()
        self.xlabel_mob.position = [pos.x,-self.xl_offset]

        self.dot.position = pos
        self.about_point = pos
        self.position=pos

    @property
    def xlabel(self):
        return self.xlabel_mob.text

    @property
    def ylabel(self):
        return self.ylabel_mob.text

    @property
    def xline_opacity(self):
        return self._xline_opacity

    @property
    def yline_opacity(self):
        return self._yline_opacity

    @property
    def xlabel_opacity(self):
        return self._xlabel_opacity

    @property
    def ylabel_opacity(self):
        return self._ylabel_opacity

    @property
    def dot_fill_opacity(self):
        return self._dot_fill_opacity

    @property
    def dot_stroke_opacity(self):
        return self._dot_stroke_opacity

    @property
    def dot_opacity(self):
        return self._dot_opacity

    @property
    def opacity(self):
        return self._opacity

    @xline_opacity.setter
    def xline_opacity(self,opacity):
        self._xline_opacity = opacity
        self.opacity = self._opacity

    @yline_opacity.setter
    def yline_opacity(self,opacity):
        self._yline_opacity = opacity
        self.opacity = self._opacity

    @xlabel_opacity.setter
    def xlabel_opacity(self,opacity):
        self._xlabel_opacity = opacity
        self.opacity = self._opacity

    @ylabel_opacity.setter
    def ylabel_opacity(self,opacity):
        self._ylabel_opacity = opacity
        self.opacity = self._opacity

    @dot_fill_opacity.setter
    def dot_fill_opacity(self,opacity):
        self._dot_fill_opacity = opacity
        self.opacity = self._opacity

    @dot_stroke_opacity.setter
    def dot_stroke_opacity(self,opacity):
        self._dot_stroke_opacity = opacity
        self.opacity = self._opacity

    @xlabel.setter
    def xlabel(self,text):
        self.xlabel_mob.text = text
        self.marker_pos = self.position


    @ylabel.setter
    def ylabel(self,text):
        self.ylabel_mob.text = text
        self.marker_pos = self.position

    @dot_opacity.setter
    def dot_opacity(self,opacity):
        self._dot_opacity = opacity
        self.opacity = self._opacity

    @opacity.setter
    def opacity(self,value):
        self._opacity=value
        self.xline.stroke_opacity=self.xline_opacity*value
        self.yline.stroke_opacity=self.yline_opacity*value
        self.dot.fill_opacity=self.dot_fill_opacity*self.dot_opacity*value
        self.dot.stroke_opacity=self.dot_stroke_opacity*self.dot_opacity*value
        self.xlabel_mob.opacity = self.xlabel_opacity*value
        self.ylabel_mob.opacity = self.ylabel_opacity*value

