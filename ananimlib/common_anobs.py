# -*- coding: utf-8 -*-
"""
A small collection of basic AnObjects

Created on Wed Nov 20 15:23:10 2019
@author: gtruch

"""

import ananimlib as al

import copy as cp
import numpy as np

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


class Line(al.BezierAnObject):
    """A straight line.

    Parameters
    ----------
    point 1 : Vector
        The coordinates of the first end point

    point 2 : Vector
        The coordinates of the second end point
    """
    def __init__(self,point1,point2,pen=None):
        super().__init__(pen=pen)

        self._point1 = al.Vector(point1)
        self._point2 = al.Vector(point2)

        self._build()
        


    @property
    def point1(self):
        return self._point1

    @point1.setter
    def point1(self, newpoint):
        self._point1 = al.Vector(newpoint)
        self._build()

    @property
    def point2(self):
        return self._point2

    @point2.setter
    def point2(self, newpoint):
        self._point2 = al.Vector(newpoint)
        self._build()

    def _build(self):
        path = al.PolyBezier()
        path.connect_linear([self._point1,self._point2])

        self.data=path



class Circle(al.BezierAnObject):
    """A Circle

    Parameters
    ----------
    radius : float
        The radius of hte circle

    coordinates : Coordinates, optional
        An instance of a Coordinates object containing the initial position
        and orientation the circle.

    pen : Pen
        An instance of a Pen object with rendering instructions

    """

    def __init__(self,radius,e=0.0,pen=None,coordinates=None):
        """Create the circle"""

        super().__init__(pen=pen)
        self.e=e
        self.radius=radius

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self,radius):
        self._radius = radius
        self._build_circle()

    def _build_circle(self):
        angle = np.arange(-45,360+90,45)*np.pi/180

        a = self.radius
        b = a*np.sqrt(1-self.e**2)
        path = al.PolyBezier()

        path.connect_smooth(np.array([
            a*np.cos(angle),
            b*np.sin(angle)]
        ).transpose())

        path._data = path._data[1:-1,:,:]

        self.data = path

class Dot(Circle):
    """A solid dot (filled in circle)
    
    Parameters
    ----------
    radius : optional float
        The radius of the dot.
        default = 0.1
        
    pen : optional Pen
        The pen used to draw the dot
        default = A pleasing (to me) color
    """
    
    def __init__(self,radius=0.1,pen=None):
        if pen is None:
            pen = al.Pen(fill_color="#cda448", fill_opacity=1.0)
            super().__init__(radius,pen=pen)

class Arc(Circle):
    """A circular arc

    Parameters
    ----------
    radius : float
        Radius of curvature

    start_angle : float
        The angle in radians wrt the x-axis where the arc starts

    stop_angle : float
        The angle in radians wrt the x-axis where the arc stops
    """

    def __init__(self,radius,start_angle, stop_angle, e=0.0, pen=None):
        super().__init__(radius,e=e,pen=pen)
        
        self._start_angle=start_angle
        self._stop_angle=stop_angle
        
        # Save the original circle
        self.circle = self.data
        
        self._build()
        

    @property
    def start_angle(self):
        return self._start_angle
    
    @property
    def stop_angle(self):
        return self._stop_angle
    
    @start_angle.setter
    def start_angle(self,val):
        self._start_angle = val
        self._build()
        
    @stop_angle.setter
    def stop_angle(self,val):
        self._stop_angle = val
        self._build()

    def _build(self):

        _,new = self.circle.split(self.start_angle/(2*np.pi))

        new,_ = new.split((self.stop_angle-
                           self.start_angle)/(2*np.pi-self.start_angle))

        self.data = new


class Arrow(al.CompositeAnObject):
    """A basic arrow consisting of a line with a pointy tip.

    Provides several positioning helpers.

    Attributes
    ----------
    start, end : Vector
        The start and end points of the arrow.
        Start is the tail, end is the head.


    pen, head_pen : optional Pen
        The pen used to draw the arrow
    """

    def __init__(self,tail_pos,head_pos,head_size=1.0,
                 pen=None,
                 head_pen=None):

        super().__init__()

        tpos = al.Vector(tail_pos)
        hpos = al.Vector(head_pos)
        self.head_size=head_size


        # Find magnitude and angle of the arrow
        self._magnitude     = (hpos-tpos).r
        self.rotation_angle = (hpos-tpos).theta

        if pen is None:
            pen = al.Pen()

        if head_pen is None:
            head_pen=al.Pen(stroke_opacity=0.0,
                               stroke_width=pen.stroke_width,
                               fill_color=pen.stroke_color,
                               fill_opacity=pen.stroke_opacity)

        self.head_pen = head_pen
        self.pen = pen

        # Create the arrow components
        head = ArrowHead(pen=head_pen,size=head_size)
        tail = al.BezierAnObject(pen=pen)

        self.add_anobject(tail,'tail')
        self.add_anobject(head,'head')

        self._build_arrow()
        self.about_point = [0.0,0.0]
        self.position = tpos

    def about_tail(self):
        """Position changes and rotations are about the tail of the arrow."""
        self.about_point = [0,0]

    def about_head(self):
        """Position changes and rotations are about the head of the arrow."""
        self.about_point = [self.magnitude,0]

    @property
    def head_pos(self):
        """Position of the head of the arrow in Scene Cooordinates."""
        return self.internal2external(al.Vector(self.magnitude,0))

    @property
    def tail_pos(self):
        """Position of the tail of the arrow in Scene Cooordinates."""
        return self.internal2external(al.Vector(0,0))

    @property
    def magnitude(self):
        return self._magnitude

    @magnitude.setter
    def magnitude(self,mag):
        self._magnitude = mag
        self._build_arrow()


    @head_pos.setter
    def head_pos(self,head_pos):
        """Move the head of the arrow leaving the tail in place.

        Parameters
        ----------
        pos : iterable of floats
            The Scene Space cartesian coordinates of the end of the arrow
        """
        head_pos = al.Vector(head_pos)
        diff = head_pos-self.tail_pos
        self.magnitude      = diff.r
        self.rotation_angle = diff.theta
        self._build_arrow()
        self.about_head()
        self.position       = head_pos

    @tail_pos.setter
    def tail_pos(self,tail_pos):
        """Move the tail of the arrow leaving the head in place"""

        tail_pos = al.Vector(tail_pos)
        head_pos = cp.copy(self.head_pos)

        diff = head_pos - tail_pos

        self.magnitude     = diff.r
        self.rotation_angle = diff.theta
        self._build_arrow()
        self.about_head()
        self.position = head_pos

    @property
    def arrow_width(self):
        return self.get_anobject('tail').stroke_width

    @arrow_width.setter
    def arrow_width(self,width):
        self.get_anobject('tail').stroke_width=width


    @property
    def opacity(self):
        return self.get_anobject('tail').stroke_opacity

    @opacity.setter
    def opacity(self,value):
        self.get_anobject("tail").stroke_opacity=value
        self.get_anobject("head").fill_opacity=value

    @property
    def color(self):
        return self.get_anobject("tail").stroke_color

    @color.setter
    def color(self,value):
        self.get_anobject("tail").stroke_color=value
        self.get_anobject("head").fill_color=value


    def _build_arrow(self):

        head = self.get_anobject('head')
        tail = self.get_anobject('tail')

        # Lay the arrow natively on the x-axis
        # with its tail at the origin
        tail.data = al.PolyBezier()
        tail.data.connect_linear(
                    [[                         0, 0],
                     [self.magnitude-head.length, 0]])

        # Put the head at the front end of the tail
        head.about_right()
        head.position      = [self.magnitude,0]


class DoubleArrow(Arrow):



    def _build_arrow(self):


        if not 'head2' in self.data.keys:
            head2 = ArrowHead(pen=self.head_pen,size=self.head_size)
            self.add_anobject(head2,'head2')
        else:
            head2 = self.get_anobject('head2')

        head = self.get_anobject('head')
        tail = self.get_anobject('tail')

        # Lay the arrow natively on the x-axis
        # with its tail at the origin
        tail.data = al.PolyBezier()
        tail.data.connect_linear(
                    [[              head2.length, 0],
                     [self.magnitude-head.length, 0]])

        # Put the head at the front end of the tail
        head.about_right()
        head.position      = [self.magnitude,0]

        head2.about_right()
        head2.rotation_angle = np.pi
        head2.position=[0,0]


class ArrowHead(al.BezierAnObject):

    def __init__(self,length=0.2,width=0.15,back=0.05,size=1.0,pen=None):
        super().__init__(pen=pen)

        self.size=size
        self.o_length =length
        self.o_width  = width
        self.o_back   = back

        self._build_head()


    def set_head_size(self,size):
        self.size = size
        self._build_head()

    def _build_head(self):
        self.length = self.o_length*self.stroke_width*self.size
        self.width  = self.o_width*self.stroke_width*self.size
        self.back   = self.o_back*self.stroke_width*self.size

        tl,tw,tb = np.array((self.length,self.width,self.back))

        # Build the arrowhead
        path = al.PolyBezier()
        path.connect_smooth([[-tb,-tw/2], [0, 0],[-tb, tw/2]])
        path.connect_linear([[-tb, tw/2,],[tl,0],[-tb,-tw/2]])

        self.data = path


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
        rect = Rectangle(size,pen=background_pen)
        rect.about_lower()
        rect.about_left()
        rect.position = [0.0,0.0]

        # Main grid
        mgsize =[size[0]*(1-lm-rm),size[1]*(1-tm-bm)]
        grid = Grid(mgsize,al.Vector([1/gridDensity,1/gridDensity]),pen=grid_pen)
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


class Rectangle(al.BezierAnObject):
    """A rectangle."""

    def __init__(self,size, pen=None, coordinates=None):
        """Initialize the rectangle

        Parameters
        ----------
        size : iterable of floats
            The size of the rectangle as [dx,dy,dz]

        position : optional iterable of floats
            The position of the center of the rectangle
            default: [0.0,0.0]
        """

        # Initialize the path
        self.data = al.PolyBezier()
        self.size = al.Vector(size)

        super().__init__(self.data, pen)

        if coordinates is None:
            self.about_center()
            self.position = [0.0,0.0]

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self,value):
        self._size = al.Vector(value)
        self._build_rectangle()

    def  _build_rectangle(self):
        
        # Center the rectangle on [0,0]
        ll = self.size*[-0.5,-0.5,0.0]
        ul = self.size*[-0.5,0.5,0.0]
        ur = self.size*[0.5,0.5,0.0]
        lr = self.size*[0.5,-0.5,0.0]
        
        self.data = al.PolyBezier()
        self.data.connect_linear([ll,ul,ur,lr,ll])
            # [ml.Vector(          0, 0     ),      # ll
            #                      ml.Vector(           0, self._size.y), # ul
            #                      ml.Vector(self._size.x, self._size.y), # ur
            #                      ml.Vector(self._size.x, 0     )],      # lr
            #                      close=True)

class Grid(al.BezierAnObject):
    """A grid of lines.

    Attributes
    ----------
    size : array of float
        The size of the grid: [sx, sy]

    spacing : array of float
        The x and y grid spacing

    """

    def __init__(self,size,spacing,offset=None,pen=None):

        if len(size) == 1:
            size = al.Vector([size,size])
        else: 
            size = al.Vector(size)
            
        if offset is None:
            offset = al.Vector([0,0])
        else:
            offset = al.Vector(offset)

        path = al.PolyBezier()
        
        start = -np.floor((size/2+offset)/spacing)*spacing + offset
        end = start + size

        # Horizontal lines
        for ypos in np.arange (start[1],end[1],spacing[1]):
            path.connect_linear([[-size[0]/2, ypos],
                                 [ size[0]/2, ypos]])
            
        # Vertical lines
        for xpos in np.arange(start[0],end[0],spacing[0]):
            path.connect_linear([[xpos, -size[1]/2],
                                 [xpos, size[1]/2]])


        super().__init__(path,pen)


class CrossHair(al.BezierAnObject):
    """A crosshair"""

    def __init__(self,size=0.25,pen=None,coordinates=None):

        if pen is None:
            pen = al.Pen(stroke_width=0.75)

        try:
            iter(size)
        except:
            size = [size,size]


        # Initialize the path
        path = al.PolyBezier()
        path.connect_linear([al.Vector(-size[0]/2,0),al.Vector(size[0]/2,0)])
        path.connect_linear([al.Vector(0,-size[1]/2),al.Vector(0,size[1]/2)])


        super().__init__(path, pen)

