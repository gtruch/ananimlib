# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 14:44:18 2022

@author: Fred
"""

import ananimlib as al

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

        line = al.BezierAnobject(pen = al.Pen(fill_opacity=1.0))
        line.data.connect_linear(data)

        label = al.Number("%.2f"%(length))
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
