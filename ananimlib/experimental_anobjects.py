# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 14:44:18 2022

@author: Fred
"""
import numpy     as np
import ananimlib as al


class PlotGrid(al.CompositeAnObject):
    def __init__(self,size,
                     xrange,
                     yrange,
                     major_spacing,
                     minor_spacing=None,
                     xlabel=None,
                     ylabel=None,
                     major_pen=None,
                     minor_pen=None,
                     text_pen=None,
                     axis_pen=None):
    
        super().__init__()
        grid = al.CoordGrid2(size,xrange,yrange,major_spacing,minor_spacing)
        self.add_anobject(grid,"grid")


        # Set up the labels
        self._xlabel = None
        if xlabel is not None:
            self.xlabel = xlabel
            
        self._ylabel = None
        if ylabel is not None:
            self._ylabel = ylabel

        # List of markers
        self.markers = []

        # List of plots
        self.plots = []

    # pass through properties for the grid
    @property
    def major_spacing(self):
        return self["grid"].major_spacing
    
    @major_spacing.setter
    def major_spacing(self,other):
        self["grid"].major_spacing = other

    @property
    def minor_spacing(self):
        return self["grid"].minor_spacing
    
    @minor_spacing.setter
    def minor_spacing(self,other):
        self["grid"].minor_spacing = other

    @property
    def xrange(self):
        return self["grid"].xrange
    
    @xrange.setter
    def xrange(self,value):
        self["grid"].xrange = value
        self._range_update()

    @property
    def yrange(self):
        return self["grid"].yrange
    
    @yrange.setter
    def yrange(self,value):
        self["grid"].yrange = value
        self._range_update()

    @property
    def xlabel(self):
        return self._xlabel
    
    @xlabel.setter
    def xlabel(self,other):
        if self._xlabel is not None:
            self.remove_anobject(self._xlabel)

        self._xlabel=al.TexMath(other)
        self.xlabel.scale = 0.75
        self.xlabel.position = self["grid"].internal2external(
                                al.Vector([0.5*np.sum(self.xrange),-0.5]))
        
        self.add_anobject(self.xlabel,update_position=False)


    @property
    def ylabel(self):
        return self._ylabel
    
    @ylabel.setter
    def ylabel(self,other):
        if self._ylabel is not None:
            self.remove_anobject(self._ylabel)
        self._ylabel=al.TexMath(other)

        self.ylabel.scale = 0.75
        self.ylabel.position = self["grid"].internal2external(
                                al.Vector([0, 0.5*np.sum(self.yrange)]))-al.Vector([.75,0])
        self.add_anobject(self.ylabel,update_position = False)
        self.ylabel.rotation_angle = np.pi/2


    @property
    def size(self):
        return self["grid"].size
    
    @size.setter
    def size(self,other):
        self["grid"].size = other

    def plot(self,func,xrange = None, name=None, pen=None):
        """Plot a function

        Parameters
        ----------
        func : callable
            A function that takes a single float argument and returns a float
            or a vector of floats.

        pen : Pen
            The pen to use for the plot

        Returns
        -------
        None.

        """
        if xrange is None:
            xrange = self.xrange
        
        plot = al.ParametricFunction(func,xrange[0],xrange[1],pen=pen)

        # Set the clip region to the plot area
        clip_path = al.PolyBezier()
        clip_path.connect_linear([[xrange[0],self.yrange[0]],
                                    [xrange[1],self.yrange[0]],
                                    [xrange[1],self.yrange[1]],
                                    [xrange[0],self.yrange[1]],
                                    [xrange[0],self.yrange[0]]])
        plot.clip = clip_path


        self["grid"].add_anobject(plot, key=name,update_transform=False,maintain_stroke=True)

        if name is not None:
            self.plots.append(name)

        plot.position = [0,0]
    
    def add_marker(self,position,name,axis_pos=None):
        """Add a marker to the plot

        Parameters
        ----------
        position : Vector
            The position of the marker in user coordinates

        name : str
            The name of the marker

        Returns
        -------
        None.

        """
        marker = PlotMarker(axis_pos=axis_pos,xlabel=name)
        self["grid"].add_anobject(marker,name)
        marker.marker_position = position
        self.markers.append(name)

        


    def _range_update(self):

        # Update the markers
        for marker in self.markers:
            self["grid",marker].axis_pos = [self.xrange[0],self.yrange[0]]

        # Update the plot clip region 
        for plot in self.plots:
            clip_path = al.PolyBezier()
            clip_path.connect_linear([[self.xrange[0],self.yrange[0]],
                                        [self.xrange[1],self.yrange[0]],
                                        [self.xrange[1],self.yrange[1]],
                                        [self.xrange[0],self.yrange[1]],
                                        [self.xrange[0],self.yrange[0]]])
            self["grid",plot].clip = clip_path

class CoordGrid2(al.CompositeAnObject):

    def __init__(self,size,
                     xrange,
                     yrange,
                     major_spacing,
                     minor_spacing=None,
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
        
        # dictionary of flags to track scale changes
        self.flags = {}

        self._size          = al.Vector(size)
        self._xrange        = al.Vector(xrange)
        self._yrange        = al.Vector(yrange)
        self._major_spacing = al.Vector(major_spacing)

        if minor_spacing is None:
            self._minor_spacing=self.major_spacing/4
        else:
            self._minor_spacing = al.Vector(minor_spacing)


            

        self._opacity = 1.0
        self._major_opacity = 0.75
        self._minor_opacity = 0.5

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
        
        self.init = False    
        self._build()
        self.init = True
        

    @property
    def major_spacing(self):
        return self._major_spacing
    
    @major_spacing.setter
    def major_spacing(self,other):
        self._major_spacing = other
        self._rescale()

    @property
    def minor_spacing(self):
        return self._minor_spacing
    
    @minor_spacing.setter
    def minor_spacing(self,other):
        self._minor_spacing = other
        self._rescale()

    @property
    def xrange(self):
        return self._xrange
    
    @xrange.setter
    def xrange(self,value):
        self._xrange = al.Vector(value)
        self._rescale()
            
    @property
    def yrange(self):
        return self._yrange
    
    @yrange.setter
    def yrange(self,value):
        self._yrange = al.Vector(value)
        self._rescale()
        

    @property
    def size(self):
        return self._size
    
    @size.setter
    def size(self,other):
        self._size = other
        self._rescale()
        
        
    def _rescale(self):
        self._build()

    def _build(self):
        
        if self.init:

            # Teardown known local elements
            self.remove_anobject("major")
            self.remove_anobject("minor")
            self.remove_anobject("axis")
            for label in self.text_labels:
                self.remove_anobject(label)
    
    
            # if self.xlabel is not None:
            #     self.remove_anobject(self.xlabel)
            
        old_anobjects = self.clear()    


        grid_size = al.Vector([self.xrange[1]-self.xrange[0], 
                               self.yrange[1]-self.yrange[0]])
        
        center = al.Vector([0.5*np.sum(self.xrange),0.5*np.sum(self.yrange)])

        old_pos = self.position
        
        scale = self.size*grid_size**-1.0
        self.scale = scale
        

        # Create the major grid lines 
        major = al.Grid2(self.xrange*scale[0], 
                         self.yrange*scale[1], 
                         self.major_spacing*scale, 
                         pen=self.major_pen)

        # Create the minor grid lines 
        minor = al.Grid2(self.xrange*scale[0], 
                         self.yrange*scale[1], 
                         self.minor_spacing*scale, 
                         pen=self.minor_pen)

        self.add_anobject(minor,    "minor", update_position=False)
        self.add_anobject(major,    "major", update_position=False)
        # self.add_anobject(outline,"outline", update_transform=False)


        # Place the coordinate axis
        axis_path = al.PolyBezier()

        # x-axis
        if self.yrange[0] <= 0 and self.yrange[1] >= 0:
            ypos = 0
        elif self.yrange[0] < 0: 
            ypos = self.yrange[1]
        else:
            ypos = self.yrange[0]
        axis_path.connect_linear([[self.xrange[0]*scale[0],ypos*scale[1]],
                                  [self.xrange[1]*scale[0],ypos*scale[1]]])

        # y-axis
        if self.xrange[0] <= 0 and self.xrange[1] >= 0:
            xpos = 0
        elif self.xrange[0] < 0: 
            xpos = self.xrange[1]
        else:
            xpos = self.xrange[0]
        axis_path.connect_linear([[xpos*scale[0], self.yrange[0]*scale[1]],
                                  [xpos*scale[0], self.yrange[1]*scale[1]]])


        axis = al.BezierAnObject(axis_path,pen=self.axis_pen)
        self.add_anobject(axis,"axis", update_position=False)



        start_coord = al.Vector([self.xrange[0],self.yrange[0]])
        end_coord   = al.Vector([self.xrange[1],self.yrange[1]])

        start_num = np.ceil(start_coord*self.major_spacing**-1)
        end_num   = np.floor(end_coord*self.major_spacing**-1)+1

        # Create x-axis tick labels at the major grid lines. 
        self.text_labels = []
        labels = al.CompositeAnObject()
        for num in np.arange(start_num[0],end_num[0])*self.major_spacing[0]:
            _num = repr(np.round(num,3))
            text = al.Text(_num,pen=self.text_pen)
            text.position = [num,-0.17/scale[1]+ypos]
            text.scale = 0.3
#            text.scale = [0.3*self.scale[1]/self.scale[0], 0.3]
            self.add_anobject(text,update_position=False)
            self.text_labels.append(text)

        # y-axis tick labels
        for num in np.arange(start_num[1],end_num[1]+1)*self.major_spacing[1]:
            text = al.Text(repr(round(num,3)),pen=self.text_pen)
            text.about_right()
            text.position = [-(0.1)/scale[0]+xpos,num]
            text.scale = 0.3
#            text.scale = [0.3*self.scale[1]/self.scale[0],0.3]
            self.add_anobject(text,update_position=False)
            self.text_labels.append(text)
            
        
        # Put external elements back using the proper flag
        for anob,key,flags in old_anobjects:
            self.add_anobject(anob, 
                    key=key,
                    update_transform = True,
                    update_position  = flags['update_position'],
                    update_scale     = flags['update_scale'],
                    maintain_stroke  = flags['maintain_stroke'])
            if hasattr(anob, 'plt_rescale'):
                anob.plt_rescale()
        
        self.about_point = center
        self.position = old_pos

#    def _build_grid(self,)


class PlotMarker(al.CompositeAnObject):
    
    
    def __init__(self,axis_pos=None,xlabel=None,ylabel=None):
        super().__init__()        

        xpen = al.Pen(stroke_color   = "#82C1FE",
                      stroke_width   = 2.0,
                      stroke_opacity = 0)

        ypen = al.Pen(stroke_color   = "#9c41cd",
                      stroke_width   = 2.0,
                      stroke_opacity = 0.95)
        
        if axis_pos is None:
            self._axis_pos = al.Vector([0,0])
        else: 
            self._axis_pos = al.Vector(axis_pos)
        
        self._marker_position = [0,0]
        self._xlabel_text = xlabel
        self._ylabel_text = ylabel
        self._xlabel = None
        self._ylabel = None


        self.dot = al.Dot()
        self.xline = al.Line([0,0], [1,0],pen=xpen)
        self.yline = al.Line([0,0],[0,1],pen=ypen)
        self.add_anobject(self.xline,"xline")
        self.add_anobject(self.yline,"yline")
        self.add_anobject(self.dot)

        self._xlabel_scale = .75
        self._ylabel_scale = .75
        self._xlabel_offset = 0.2
        self._x_ap_offset = 0.7

        self._build()
        
    @property
    def xlabel(self):
        return self._xlabel
    
    @xlabel.setter
    def xlabel(self,other):
        if self._xlabel is not None:
            self.remove_anobject(self._xlabel)

        self._xlabel_text = other
        self._xlabel = al.TexMath(other)
        self._xlabel.scale = 6.0
        self._xlabel.about_center()
        self.add_anobject(self._xlabel,"xlabel")
        
        self._build()

    @property
    def ylabel(self):
        return self._ylabel
    
    @ylabel.setter
    def ylabel(self,other):
        if self._ylabel is not None:
            self.remove_anobject(self._ylabel)

        self._ylabel = al.TexMath(other)
        self._ylabel.about_center()
        self.add_anobject(self._ylabel,"ylabel")
        
        self._build()

    @property 
    def xlabel_scale(self):
        return self._xlabel_scale
    
    @xlabel_scale.setter
    def xlabel_scale(self, scale):
        self._xlabel_scale = scale
        
        if self._xlabel is not None: 
            self._xlabel.scale = self._xlabel_scale
            self._build()

    @property 
    def ylabel_scale(self):
        return self._ylabel_scale
    
    @xlabel_scale.setter
    def ylabel_scale(self, scale):
        self._ylabel_scale = scale
        
        if self._ylabel is not None: 
            self._ylabel.scale = self._ylabel_scale
            self._build()

    @property
    def axis_pos(self):
        return self._axis_pos
    
    @axis_pos.setter
    def axis_pos(self, other):
        self._axis_pos = al.Vector(other)
        self._build()
        
    
    @property
    def marker_position(self):
        return self._marker_position
    
    @marker_position.setter
    def marker_position(self,other):
        self._marker_position = al.Vector(other)
        self._build()
    
    def plt_rescale(self):
        self._build()
    

    def _build(self):
        
        
        # pos = self.internal2external(self.marker_position)
        # ap = self.internal2external(self.axis_pos)
        
        pos = self.external2internal(self.marker_position)
        ap = self.external2internal(self.axis_pos)

        # pos = self.marker_position
        # ap  = self.axis_pos 

        self.dot.position = pos
        self.xline.point1 = pos
        self.xline.point2 = [ap[0],pos[1]]
        
        if self.xlabel is not None:
            self.xlabel.about_upper
            self.xlabel.position = [pos[0],ap[1]-self._xlabel_offset - self._x_ap_offset]
            self.xlabel.scale = self._xlabel_scale
            
        if self.ylabel is not None:
            self.ylabel.about_right()
            self.ylabel.position = [ap[0]-0.1,pos[1]]
            self.ylabel.scale = self._ylabel_scale
        
        self.yline.point1 = pos
        self.yline.point2 = [pos[0],ap[1]-self._x_ap_offset]
        

class Grid2(al.BezierAnObject):
    """A grid of lines.

    Attributes
    ----------
    size : array of float
        The size of the grid: [sx, sy]

    spacing : array of float
        The x and y grid spacing

    """

    def __init__(self,xrange,yrange,spacing,offset=None,pen=None):


        xrange = al.Vector(xrange)
        yrange = al.Vector(yrange)
        spacing = al.Vector(spacing)

        path = al.PolyBezier()
        
        start_coord = al.Vector([xrange[0],yrange[0]])
        end_coord   = al.Vector([xrange[1],yrange[1]])
        
        start_num = np.ceil(start_coord*spacing**-1)
        end_num   = np.floor(end_coord*spacing**-1)+1
        

        # Horizontal lines
        for ynum in np.arange(start_num[1],end_num[1]+1,1):
            path.connect_linear([[xrange[0], ynum*spacing[1]],
                                 [xrange[1], ynum*spacing[1]]])
            
        # Vertical lines
        for xnum in np.arange(start_num[0],end_num[0],1):
            path.connect_linear([[xnum*spacing[0], yrange[0]],
                                 [xnum*spacing[0], yrange[1]]] )

        super().__init__(path,pen)
    

class ParametricFunction(al.BezierAnObject):
    """A parametric function"""
    
    
    def __init__(self,func,start_param,end_param,num_samples=50,pen=None):
        """
        

        Parameters
        ----------
        func : callable
            A callable that takes a vector of n floats and returns an nx3 
            matrix of output values.
            
        start_param : float
            The initial value of the independent variable
            
        end_param : float
            the final value of the independent variable
            
        num_samples : int, optional
            The number of samples in the interval The default is 50.

        """
        
        self.func        = func
        self._start_param = start_param
        self._end_param   = end_param
        self.num_samples = num_samples
        
        self.rebuild_path()
        
        super().__init__(self.path,pen=pen)
        
    @property
    def start_param(self):
        return self._start_param
    
    @start_param.setter
    def start_param(self, other):
        self._start_param = other
        self.rebuild_path()

    @property
    def end_param(self):
        return self._end_param
    
    @end_param.setter
    def end_param(self, other):
        self._end_param = other
        self.rebuild_path()
        
    def f(self, x):
        """The output value for any given input value"""
        
        # result = self.func(np.array([x]))
        # return result[1,0]
        return self.func(x)
    
    def rebuild_path(self):
        x = np.linspace(self.start_param,self.end_param,self.num_samples)
        out = np.array([[_x,self.func(_x),0] for _x in x])
                
        self.path = al.PolyBezier()
        self.data = self.path
        self.path.connect_smooth(out)



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

class R_Triangle(al.BezierAnObject):

    def __init__(self,vertex,pen=None):

        self._vertex = al.Vector(vertex)
        path = al.PolyBezier()
        path.connect_linear([[0,0],
                            [self._vertex.x,self._vertex.y],
                            [self._vertex.x,0],
                            [0,0]])

        super().__init__(path,pen)

    @property
    def vertex(self):
        return self._vertex

    @vertex.setter
    def vertex(self,vertex):
        self._vertex = al.Vector(vertex)
        path = al.PolyBezier()
        path.connect_linear([[0,0],[vertex.x,vertex.y],[vertex.x,0],[0,0]])
        self.data = path

class Dimension(al.CompositeAnObject):    
    '''A marker for showing length on a digram
    
    Attributes
    ----------
    label : String
        The text to show in the dimension marker
        
    start : Vector
        The starting point (left tip)
        
    end : Vector
        The ending point (right tip)
    '''
    
    def __init__(self,label,start,end):
        super().__init__()
        
        self._start = al.Vector(start)
        self._end   = al.Vector(end)        
        self.label  = label
        self._label_scale = 1.0
        self._build()
                
    @property
    def label_scale(self):
        return self._label_scale
    
    @label_scale.setter
    def label_scale(self,scale):
        self._label_scale=scale
        self._build()

    @property
    def start(self):
        return self._start
    
    @start.setter
    def start(self,other):
        self._start = al.Vector(other)
        self._build()
        
    @property
    def end(self):
        return self._end
    
    @end.setter
    def end(self,other):
        self._end = al.Vector(other)
        self._build()

    @property 
    def length(self):
        return (self.end-self.start).mag
    
    @length.setter
    def length(self,other):
        disp = self.end-self.start
        disp.mag = other
        self.end = self.start+disp
        self._build()
        
    @property        
    def opacity(self):
        return self._opacity
    
    @opacity.setter
    def opacity(self, other):
        self._opacity = other
        self.set_attributes('opacity', other)
        

    def _build(self):
            start = self.start
            end   = self.end
            label = self.label
    
            self.clear()        
            self.position = [0,0]
            
            length = (end-start).mag
            
            self.label_ob = al.TexMath(label)
            self.label_ob.scale = self._label_scale
            self.label_ob.position = [length/2,0]
            bb = self.label_ob.bounding_box
            label_width = bb[1,0]-bb[0,0]
            label_height = bb[1,1]-bb[0,1]
            
                    
            self.left_arrow  = al.Arrow([length/2-label_width/2,0], [0,0])
            self.right_arrow = al.Arrow([length/2+label_width/2,0], [length,0])
            
            self.left_limit  = al.Line([0,-label_height/2], [0,label_height/2])
            self.right_limit = al.Line([length,-label_height/2], 
                                       [length,label_height/2])
            
            self.add_anobject(self.left_arrow)
            self.add_anobject(self.right_arrow)
            self.add_anobject(self.label_ob)
            self.add_anobject(self.left_limit)        
            self.add_anobject(self.right_limit)
            
            self.about_left()
            self.position = start
            self.rotation_angle = (end-start).theta

class Dimension2(al.CompositeAnObject):
    """A dimension bracket with a label

    Attributes
    ----------

    left : Vector
        The coordinates of the left pointer

    right : Vector
        The coordinates of the right pointer
    """

    def __init__(self,left_point, right_point):
        super().__init__()

        self._left_point = al.Vector(left_point)
        self._right_point = al.Vector(right_point)

        self._build_dimension()

    @property
    def length(self):
        return (self._right_point - self._left_point).r

    @property
    def left_point(self):
        return self._left_point

    @property
    def right_point(self):
        return self._right_point

    @left_point.setter
    def left_point(self,point):
        self._left_point = point
        self._build_dimension()

    @right_point.setter
    def right_point(self,point):
        self._right_point = point
        self._build_dimension()

    def _build_dimension(self):
        self.clear()    # Throw out the old anobjects
        length = self.length
        self.position = [0.0,0.0]
        self.rotation_angle = 0.0

        data = [[0,0],             # Left
                [0.0,0.5],         # Top Left
                [length,0.5],      # Top Right
                [length,0],        # Right
                [length-0.1,0.45],  # Under right
                [0.1,0.45],         # Under left
                [0,0]]             # Left

        line = al.BezierAnObject(pen = al.Pen(fill_opacity=1.0))
        line.path.connect_linear(data)

#        label = al.Number("%.2f"%(length))
        label = al.Text("5")
        label.about_center()
        label.about_lower()
        label.position = [length/2,0.6]
        label.scale=0.5

        self.add_anobject(line)
        self.add_anobject(label)

        self.position = self._left_point
        self.rotation_angle = (self._right_point-self._left_point).theta

class EngineerPaper(al.CompositeAnObject):
    """A piece of green engineering paper to draw on"""

    def __init__(self,size=al.Vector([8.5,11.0]),gridDensity=7.0,
                 topMarg=0.04, botMarg=0.0,
                 leftMarg=0.09,rightMarg=.04):
        """Build the composite

        Parameters
        ----------
        size : Vector
            Size of the paper in Scene Units

        gridDensity : optional float
            Number of gridlines per Scene Unit
            default = 5.0

        topMarg,botMarg,leftMarg,rightMarg : float
            The margins as a percentage of the paper dimensions
        """
        super().__init__()

        # Convenience variables
        size = al.Vector(size)
        tm,bm,lm,rm = (topMarg,botMarg,leftMarg,rightMarg)
        sx,sy,_ = size

        # Create pens
        background_pen = al.Pen(fill_color="#d9f5e2",
                                   fill_opacity=1.0,
                                   stroke_opacity=0.0)

        grid_pen = al.Pen(stroke_color="#69933c",
                             stroke_opacity=0.3)

        margin_pen = al.Pen(stroke_color="#69933c",
                               stroke_opacity=1.0)

        punch_pen = al.Pen(fill_color='#000000',
                              fill_opacity=1.0,
                              stroke_opacity=0.0)

        # Main paper background
        rect = al.Rectangle(size,pen=background_pen)
        rect.about_lower()
        rect.about_left()
        rect.position = [0.0,0.0]

        # Main grid
        mgsize =[size[0]*(1-lm-rm),size[1]*(1-tm-bm)]
        grid = al.Grid(mgsize,al.Vector([1/gridDensity,1/gridDensity]),pen=grid_pen)
        grid.about_center()
        grid.rotation_angle = np.pi
        grid.about_lower()
        grid.about_right()
#        grid.position = [sx*lm,sy*(1-bm-tm)]
        grid.position = [sx*lm,sy*(1-tm-bm)]

        # Dark margin lines
        path = al.PolyBezier()
        path.connect_linear([[sx*lm,0],[sx*lm,sy]])         # left line
        path.connect_linear([[0,sy*(1-tm)],[sx,sy*(1-tm)]]) # top line
        path.connect_linear([[sx*(1-rm),0],[sx*(1-rm),sy]]) # right line

        # Weird little lines at the top of the page
        path.connect_linear([[sx*(lm + 1/3*(1-rm-lm)),sy*(1-tm)],
                               [sx*(lm + 1/3*(1-rm-lm)),sy]])
        path.connect_linear([[sx*(lm + 2/3*(1-rm-lm)),sy*(1-tm)],
                                [sx*(lm + 2/3*(1-rm-lm)),sy]])
        mgrid = al.AnObject(path, al.BezierRender(pen=margin_pen))
        mgrid.about_lower()
        mgrid.about_left()
        mgrid.position = [0,0]

        self.add_anobject(rect)
        self.add_anobject(grid)
        self.add_anobject(mgrid)

        # punch holes (5/8 of an inch)
        for y in np.array([1.375, 5.5, 9.375])/11.0:
            hole = Circle(radius=.15, pen = punch_pen)
            hole.position = [sx*lm/2,y*sy]
            self.add_anobject(hole)
