# -*- coding: utf-8 -*-
"""
Bezier Handling Routines

A collection of classes to handle creation and manipuplation
of Cubic Bezier curves.

Many algorithms adapted from "A Primer on Bezier Curves"
https://pomax.github.io/bezierinfo/

Code for SVG Paths adapted from Grant Sanderson's Manimlib

Created on Fri Oct 25 08:01:58 2019
@author: G.Ruch
"""

import ananimlib as al

import numpy as np
import scipy.linalg as linalg

import re


class PolyBezier():
    """Container for a connected  Cubic Poly-Bezier curve

    Contains a set of connected Bezier Curves, where the end point
    of the curve at n-1 is the same as the starting point of the
    curve at n.

    Attributes
    ----------
    num_segments : int
        The number of Bezier segments

    """

    def __init__(self,segments=None):
        """Initialize with an iterable of Bezier Segments

        Parameters
        ----------
        segments : List of BezierSegment
            Initial segments in the curve
        """
        self._data = None
        self._bounding_box = None

        if segments is not None:
            for seg in segments:
                self.add_segment(seg)

        self._lengths = None
        self._length = None

    @property
    def num_segments(self):
        segs,points,dims = self._data.shape
        return segs

    @property
    def points(self):
        """Return the Bezier coefficients as an n*4x3 ndarray"""

        rows,cols,dims = self._data.shape
        return self._data.reshape([rows*cols,dims])

    @points.setter
    def points(self,val):
        """Set the Bezier coefficients using an n*4x3 ndarray

        Parameters
        ----------
        val : n*4x3 ndarray of floats
            ndarray of the Bezier coefficients.

        Raises
        ------
            ValueError if the number of rows is not a multiple of four
            or if the number of columns is less than three
        """

        # Check the shape of the incoming array
        rows,cols = val.shape
        if rows%4 != 0 and cols != 3:
            raise ValueError("The number of points in a Poly Bezier must be " +
                             "a multiple of 4 and each point must have 3 " +
                             "dimensions.")

        self._data = val.reshape([int(rows/4),4,3])
        self._bounding_box = None   # Invalidate the bounding box
        self._lengths=None


    def shift(self,displacement):
        """Shift the curve's position by the desired displacement.

        Adds the displacement vector to all of the points defining the curve

        Parameters
        ----------
        displacement : Vector
            The displacement vector to add to the points
        """

        # _data is an nx4x3 cube with the spatial coordinates x,y,z along
        # the last dimension.  So the displacement vector is adjusted
        # so that the desired displacment is in the same dimension
        # so that numpy's broadcasting rules work for us.
        displacement = np.array(displacement)
        self._data = self._data + displacement[None,None,:]
        self._bounding_box = self._bounding_box + displacement


    def split(self,t):
        """Split the Bezier curve at t into two pieces.

        Let 0<=t<=1 so that it represents a portion of the entire shape.
        split finds locates the correct BezierSegment and divides it
        using BezierSegment.split

        Parameters
        ----------
        t : float
            The split point as a fraction of the total curve.  0<=t<=1
        """

        seg,tseg = self.find_segment(t)


        # Split the segment
        leftSeg,rightSeg = self[seg].split(tseg)

        # Build the left and right portions
        left = PolyBezier(self[:seg])
        left.add_segment(leftSeg)
        right = PolyBezier([rightSeg])
        for s in self[(seg+1):]:
            right.add_segment(s)

        return left,right


    def add_point(self,t):
        """Add an end point at t.  Creates another segment."""

        left,right = self.split(t)
        self.points = (left+right).points
        self._bounding_box = None   # Invalidate the bounding box
        self._lengths=None


    

    def B(self,t):
        """Calcuate the coordinates of the curve
        
        Parameters
        ----------
        t : float
            The Bezier parameter
            
        Returns
        -------
        ndarray of floats
            The coordinates of a point along the curve at t
        
        """

#        seg,tseg = self.find_segment(t)
        torg = t

#        t = t*(self.num_segments)
        if t==self.num_segments:
            seg = self.num_segments-1
        else:
            seg = int(np.floor(t))

        t = (t-seg)
        

        return self[seg].B(t)

    def T(self,p,param=0,niter=25):
        """Get the value of t the chosen coordinate.

        Behavior is undefined if the curve is not singular in the 
        chosen first coordinate.
        """

        tl = 0.0
        tr = self.num_segments
        Bl = self.B(tl)
        Br = self.B(tr)

        for indx in np.arange(niter):
            tm = 0.5*(tr+tl)
            Bm = self.B(tm)

            if (Bm[param]-p)*(Bl[param]-p) > 0:
                tl = tm
                Bl = Bm
            else:
                tr = tm
                Br = Bm

        return 0.5*(tr+tl)


    def Bprime(self,t):
        """Calcuate the coordinates of the curve with 1<=t<=0"""

#        seg,tseg = self.find_segment(t)

        torg=t
#        t = t*self.num_segments        
        t=np.round(t,5)
        seg = int(np.floor(t))
        t = (t-seg)


        return self[seg].Bprime(t)

    def Bdprime(self,t):
        """Calcuate the coordinates of the curve with 1<=t<=0"""

#        seg,tseg = self.find_segment(t)

#        t = t*self.num_segments        
        seg = int(np.floor(t))
        t = (t-seg)

        return self[seg].Bdprime(t)

    def D(self,t):

        seg,tseg = self.find_segment(t)
        return self[seg].D(np.round(tseg,6))

    def Dprime(self,t):

        seg,tseg = self.find_segment(t)
        return self[seg].Dprime(np.round(tseg,6))

    def Ddprime(self,t):

        seg,tseg = self.find_segment(t)
        return self[seg].Ddprime(np.round(tseg,6))

    @property
    def lengths(self):
        """The length of each segment"""

        # Calculate the length of each segment
        if self._lengths is None:
            self._lengths = np.array([seg.arc_length for seg in self])
        
        return self._lengths

    @property    
    def length(self):
        if self._length is None:
            self._length = np.sum(self.lengths)

        return self._length

    def find_segment(self,t):
        """Find the index and t for a segment given t for the polycurve

        Parameters
        ----------
        t : float
            T

        """

        # Calculate the total length at each segment boundary
        acc = 0
        totals = []
        for l in self.lengths:
            totals.append(l+acc)
            acc = totals[-1]
        totals = np.array(totals)

        # Normalize the total length to to 1.0
        dt = totals/totals[-1]

        # Find which segment
        if t<1.0:
            seg = np.where(dt>t)[0][0]
        else:
            seg = self.num_segments-1

        # Find proportion of the curve within the segment
        if seg>0:
            try:
                tseg = (t*totals[-1]-totals[seg-1])/self._lengths[seg]
            except:
                print("dude!")
#            tseg = (t-dt[seg-1])*totals[-1]/self._lengths[seg]
        else:
            tseg = t*totals[-1]/self._lengths[seg]

        if seg == self.num_segments:
                return self[-1].B(1.0)

        return seg,tseg

    @property
    def bounding_box(self):
        """Calculate and return coordinates of the bounding box

        Returns
        -------
        bounding_box : 2x3 ndarray of floats
            Coordinates of the lower left and upper right corners
            of a box whose sides either coincide with the curve's endpoints
            or are tangent to the curve's extremities on each axis.
        """
        if self._bounding_box is None:
            self._bounding_box = self.calc_bounding_box()
        return self._bounding_box

    @property
    def center(self):
        return al.Vector(np.sum(self.bounding_box,axis=0)/2.0)

    @property
    def upper(self):
        return self.bounding_box[1,1]

    @property
    def lower(self):
        return self.bounding_box[0,1]

    @property
    def left(self):
        return self.bounding_box[0,0]

    @property
    def right(self):
        return self.bounding_box[1,0]

    def calc_bounding_box(self):
        """Calculate the coordinates of the Bezier Curve bounding box

        Returns
        -------
        bounding_box : 2x3 ndarray of floats
            Coordinates of the lower left and upper right corners
            of a box whose sides either coincide with the curve's endpoints
            or are tangent to the curve's extremities on each axis.
        """
        if len(self) > 0:
            # Get the bounding box for each segment
            extrema = np.array([seg.bounding_box() for seg in self])
            extrema = np.concatenate((extrema[:,0,:],extrema[:,1,:]))

            # Return min and max across all segments
            return np.array([extrema.min(axis=0),extrema.max(axis=0)])
        else:
            return np.zeros((2,3))

    def add_segment(self,segment):
        """Add a Bezeir Segement to the curve

        Parameters
        ----------
        segment : BezierSegment
            The Bezier Segment to add to the curve
        """

        if self._data is None:
            self._data = segment[None,:]
        else:
            self._data = np.concatenate((self._data,segment[None,:]))

        # Invalidate the bounding box
        self._bounding_box = None
        self._length = None

    def connect_linear(self,data,close=False):
        """Connect a set of points in 3-space with straight lines

        Adds the curve to the current set of points

        Parameters
        ----------
        data : nx3 iterable of floats
            The n data points to connect

        close : optional Boolean
            Connect last point back to the first when True
            default = False
        """

        # unpack the data into a ndarray
        rawData = np.array([[c for c in p] for p in data])
        if close:
            # Copy the first point to the end of the list
            # Now here's a cryptic line of code, eh? I heart numpy.
            rawData = np.concatenate((rawData,rawData[0][None,:]),axis=0)
        n_rows,n_dims = rawData.shape

        # Pack the Bezier coefficients into an (n-1)x3x4 ndarray
        # P0 = P1 and P2 = P3 to make a straight line
        #points = np.zeros([(n_rows-1),3,4])
        #points[:,:2,0] = rawData[:-1,:2]
        #points[:,:2,1] = rawData[:-1,:2]
        #points[:,:2,2] = rawData[1:,:2]
        #points[:,:2,3] = rawData[1:,:2]

        # Pack the Bezier coefficients into an (n-1)x3x4 ndarray
        # P0 = P2 and P1 = P3 to make a straight line
        points = np.zeros([(n_rows-1),3,4])
        points[:,:2,0] = rawData[:-1,:2]
        # points[:,:2,2] = rawData[:-1,:2]
        # points[:,:2,1] = rawData[1:,:2]
        points[:,:2,3] = rawData[1:,:2]
        points[:,:2,1] = 0.5*(points[:,:2,3]+points[:,:2,0])        
        points[:,:2,2] = 0.5*(points[:,:2,3]+points[:,:2,0])        

        # Internal data structure is an (n-1)x4x3 cube
        points = points.transpose([0,2,1])
        for seg in points:
            self.add_segment(seg)
        self._bounding_box = None #self.calc_bounding_box()

    def connect_smooth(self,data):
        """Smoothly connect a set of points in 3-space with Cubic Bezier segs

        Adds the curve to the current set of points

        Apologies for the barely readable numpy code below.  At some point
        it should be reworked into an intelligible form.

        Parameters
        ----------
        data : nx3 iterable of floats
            A set of n triplets representing 3-space coordinates to be
            connected.
        """

        # unpack the data into a numpy matrix
        rawData = np.array([[c for c in p] for p in data])
        n_rows,n_dims = rawData.shape

        #########################################
        # Calculate cubic Bezier control points
        #######################################

        # Bezier control points p1 and p2 are calculated using a matrix
        # calculation
        # Mp=x
        # where M is a tri-diagonal coefficeient matrix, p is a nx1 vector of
        # either p1 or p2, and x is built from the incoming data points

        # Build the transformation matrix in ab banded form for
        # scipy.linalg.solve_banded  (see scipy docs for details)
        ab = np.zeros((3,n_rows-1))
        ab[1,:] = np.ones(n_rows-1)*4.0
        ab[1,0] = 2.0
        ab[1,-1] = 7.0
        ab[0,1:] = np.ones(n_rows-2)
        ab[2,:-1] = np.ones(n_rows-2)
        ab[2,-2] = 2.0

        # Build the x matrix
        d =rawData[:,:2]
        x = 4*d[:-1]+2*d[1:]
        x[0] = d[0]+2*d[1]
        x[-1] = 8*d[-2]+d[-1]

        # Calculate P1 and P2 control points
        P1 = linalg.solve_banded((1,1),ab,x)
        P2 = np.zeros(P1.shape)
        P2[:-1] = 2*d[1:-1]-P1[1:]
        P2[-1] = 4*P1[-1]+P1[-2]-4*d[-2]

        # Pack the resulting Bezier coefficients into an (n-1)x3x4 ndarray
        points = np.zeros([(n_rows-1),3,4])
        points[:,:2,0] = rawData[:-1,:2]
        points[:,:2,1] = P1
        points[:,:2,2] = P2
        points[:,:2,3] = rawData[1:,:2]

        # Internal data structure is an (n-1)x4x3 cube
        points = points.transpose([0,2,1])
        for seg in points:
            self.add_segment(seg)
        self._bounding_box = self.calc_bounding_box()


    def __getitem__(self,index):
        """Return a single Bezier curve from the matrix

        Parameters
        ----------
        index : int
            The index of the desired bezier curve

        Returns
        -------
        bzSeg : BezierCurve
            The desired curve
        """
        return BezierCurve(self._data[index])

    def __iter__(self):
        if self._data is not None:
            for seg in self._data:
                yield BezierCurve(seg)

    def __add__(self,other):
        new_path = PolyBezier()
        new_path.points = np.append(self.points,other.points,axis=0)
        return new_path

    def __len__(self):
        if self._data is None:
            return 0
        else:
            n_curves, n_coeff, n_dims = self._data.shape
        return n_curves


class SVGPolyBezier(PolyBezier):
    """Generate a PolyBezier curve from an SVG path string

    Adapted from Manimlib by Grant Sanderson
    """

    def __init__(self,path_string,):
        super().__init__()
        self.path_string = path_string
        self.generate_points()

    def get_path_commands(self):
        result = [
            "M",  # moveto
            "L",  # lineto
            "H",  # horizontal lineto
            "V",  # vertical lineto
            "C",  # curveto
            "S",  # smooth curveto
            "Q",  # quadratic Bezier curve
            "T",  # smooth quadratic Bezier curveto
            "A",  # elliptical Arc
            "Z",  # closepath
        ]
        result += [s.lower() for s in result]
        return result

    def generate_points(self):
        """Parse the SVG Path string and generate Bezier control points"""


        # Extract command/coordinate pairs
        pattern = "[%s]" % ("".join(self.get_path_commands()))
        pairs = list(zip(
            re.findall(pattern, self.path_string),
            re.split(pattern, self.path_string)[1:]
        ))

        # Execute the commands (create Bezier control points)
        for command, coord_string in pairs:
            self.handle_command(command, self.string_to_points(coord_string))

        # people treat y-coordinate differently
        # self.about_point = [0,0]
        # self.rotation_angle = np.pi

    def handle_command(self, command, coords):

        isLower = command.islower()
        command = command.upper()
        new_points = np.array([]).reshape(0,3)

        if command != "Z" and len(coords) == 0:
            return

        # Flip the y axis
        # For V command, only the y-coordinate is passed
        # For all other commands, the second coordinate is y
        if len(coords) > 0:
            if command != "V":
                coords[:,1] *= -1
            else:
                coords[:,0] *= -1

        # moveto
        if command == "M":
            if isLower:
                coords[0] += self.current_position

            self.current_position = coords[0] # Reset the current position
            self.start_position = coords[0]   # Start a new path

            # If there are any more coordinates on the list, assume that they
            # are lineto commands
            if isLower:
                command = 'l'
            else:
                command = 'L'
            self.handle_command(command, coords[1:])
            return

        # lineto
        elif command in ["L", "H", "V"]:  # lineto

            # Horizontal Line, keep y-coordinate
            if command == "H":
                coords[:,1] = self.current_position[1]
                if isLower:
                    coords[:,0] += self.current_position[0]

            # Vertical Line, keep x-coordinate
            elif command == "V":
                coords[:,1] = coords[:,0]
                coords[:,0] = self.current_position[0]
                if isLower:
                    coords[:,1] += self.current_position[1]
            elif isLower:
                coords += self.current_position

            # Connect points with a straight line
            self.connect_linear(np.concatenate(
                (self.current_position[None,:],coords))
            )

            # Update the current point
            self.current_position = coords[-1]
            return

        # Cubic curveto - Add a Cubic Bezier
        elif command == "C":  # curveto
            if isLower:
                coords += self.current_position
                command = "c"

            ## Add the new segment
            coeff = np.concatenate((self.current_position[None,:],coords[:3,:]))
            self.add_segment(coeff)

            self.current_position = coords[-1]

            # Add any additional segments
            self.handle_command(command, coords[3:])
            return


        elif command == "S":  # smooth curveto
            # Need the second control point from the last segment
            prev_p2 = self[-1].p2

            # Reflect through the current point to calculate first control
            # point for this segment
            p1 = 2*self.current_position-prev_p2

            # Assemble the coefficients and add the segment
            coeff = np.concatenate(
                (self.current_position[None,:], p1[None,:], coords[:2,:])
            )
            self.add_segment(coeff)

            self.current_position = coords[-1]

            # handle1 = points[-1] + (points[-1] - points[-2])
            # new_points = np.append([handle1], new_points, axis=0)
            return

        # Quadratic curveto
        elif command in ["Q", "T"]:
            raise Exception("Time to implement Q and T in SVGBezier")

        elif command == "A":  # elliptical Arc
            raise Exception("Oh Dear... Elliptical Arc in SVGBezier")

        elif command == "Z":  # closepath

            # Connect the current point with the first point in the path.
            self.connect_linear(np.concatenate(
                (self.current_position[None,:],self.start_position[None,:]))
            )
            self.current_position = self.start_position
            self.start_position = None

            return


    def string_to_points(self, coord_string):
        numbers = self.string_to_numbers(coord_string)
        if len(numbers) % 2 == 1:
            numbers.append(0)
        num_points = len(numbers) // 2
        result = np.zeros((num_points, 3))
        result[:, :2] = np.array(numbers).reshape((num_points, 2))
        return result

    def string_to_numbers(self, num_string):
        num_string = num_string.replace("-", ",-")
        num_string = num_string.replace("e,-", "e-")
        return [
            float(s)
            for s in re.split("[ ,]", num_string)
            if s != ""
        ]


    def get_original_path_string(self):
        return self.path_string



class BezierCurve():
    """Container for a Cubic Bezier Curve

    Holds the coeffcients of a Cubic Bezier curve defined by:

    B(t) = p0*(1-t)**3 + p1*((1-t)**2)*t * p2*(1-t)*(t**2) + p3*(t**3)

    Attributes
    ----------
    p0, p1, p2, p3: Vector
        The cubic Bezier coefficients.
    """

    def __init__(self,coefficients):
        """Get set up

        Parameters
        ----------
        coeff : iterable containing coefficients
            coefficients[0] = p0
            coefficients[1] = p1
            coefficients[2] = p2
            coefficients[3] = p3
        """

        # Store coefficients internally as a 4x3 ndarray
        if isinstance(coefficients,np.ndarray):
            self._coefficients = coefficients
        else:
            self._coefficients = np.array([[x for x in p]
                                           for p in coefficients])
        self._distances=None
        self._t_lookup=None

    @property
    def p0(self):
        return al.Vector(self._coefficients[0])

    @property
    def p1(self):
        return al.Vector(self._coefficients[1])

    @property
    def p2(self):
        return al.Vector(self._coefficients[2])

    @property
    def p3(self):
        return al.Vector(self._coefficients[3])

    @p0.setter
    def p0(self,val):
        self._coefficients[0] = np.array(val)

    @p1.setter
    def p1(self,val):
        self._coefficients[1] = np.array(val)

    @p2.setter
    def p2(self,val):
        self._coefficients[2] = np.array(val)

    @p3.setter
    def p3(self,val):
        self._coefficients[3] = np.array(val)

    def bounding_box(self):
        """Calculate the box (or cube in R3) that encloses the curve

        Calculated by setting dB/dt = 0 and finding the roots of the
        resulting polynomial in each axis.

        Returns
        -------
        upper_right, lower_left : ndarray of Vectors
            Vectors indicating the upper right and lower left corners of the
            bounding box
        """

        # The first derivative of B is quadratic in t, so calculate the quadratic
        # coefficients
        a0,b0,c0 = np.array([[-3.0,  9.0,-9.0, 3.0],
                             [ 6.0,-12.0, 6.0, 0.0],
                             [-3.0,  3.0, 0.0, 0.0]],
                             dtype="cdouble").dot(self._coefficients)

        t = []
        for a,b,c in zip(a0,b0,c0):
            if a != 0:
                bac = b**2-4*a*c
                t.append((1/(2*a))*(-b+np.sqrt(bac)))
                t.append((1/(2*a))*(-b-np.sqrt(bac)))
            elif b != 0:
                t.append(-c/b)

        # Consider only real roots in the range 0 <= t <= 1
        t = np.array([t1.real for t1 in t if t1>=0 and t1<=1 and t1.imag==0])
        extrema = self._coefficients[[0,3],:]
        if len(t) > 0:
            extrema = np.concatenate((extrema,self.B(t)),axis=0)

        box = np.array([extrema.min(axis=0),extrema.max(axis=0)])
        return box


    def split(self,t):
        """Split the Bezier curve at t into two pieces.

        Uses de Casteljau's algorithm to divide the curve into a left
        and a right sub curve

        Parameters
        ----------
        t : float
            The split point as a fraction of the total curve.  0<=t<=1
        """

        left = []
        right = []
        def _split(t,points):
            left.append(points[0])
            right.insert(0,points[-1])
            npoints,dims = points.shape
            newpoints = []
            if npoints == 1:
                return points[0]
            else:
                for p0,p1 in zip(points[:-1,:],points[1:,:]):
                    newpoints.append(t*p1+ (1-t)*p0)
                return _split(t,np.array(newpoints))


        _split(t,self._coefficients)

        left = np.array(left)
        right = np.array(right)

        return BezierCurve(left),BezierCurve(right)

    def B(self,t,deriv=0.0):
        """Calculate the value of the Bezier segment at t

        Calculates B(t) defined as with 0<=t<=1
        B(t) = p0*(1-t)**3 + p1*3*((1-t)**2)*t * p2*3*(1-t)*(t**2) + p3*(t**3)

        Parameters
        ----------
        t : float
            The Bezier parameter limited to 0<=t<=1

        deriv : default int
            The desired derivative.
            default = 0.0 (no derivative)

        Returns
        -------
        ndarray of floats
            The coordinates of a point along the curve at t
        """

        # Keep this check?  Throw it out?  <shrug>
        # We can calculate the curve outside of the 0 to 1 range...
        # But this check tends to catch other errors so.  Keep it for now.
        if np.any(t < 0) or np.any(t > 1):
            raise ValueError("Bezier parameter t must be between 0 and 1")


        # Matrix form of B.
        # Coefficient matrix for Bezeir polynomial
        # B = np.array([
        #     [ 1,  0,  0,  0],
        #     [-3,  3,  0,  0],
        #     [ 3, -6,  3,  0],
        #     [-1,  3, -3,  1]])

        B = np.array(
            [[-1,  3, -3, 1],
             [ 3, -6,  3, 0],
             [-3,  3,  0, 0],
             [ 1,  0,  0, 0]
            ])

        tv = np.array([t**3, t**2, t**1, t**0]).transpose()
#        tv = np.array([t**0, t**1, t**2, t**3]).transpose()
        P = self._coefficients


        return tv.dot(B.dot(P))


    def Bprime(self,t):
        Bp = np.array([
            [-3,   9, -9, 3],
            [ 6, -12,  6, 0],
            [-3,   3,  0, 0],
        ])

        tv = np.array([t**2, t**1, t**0]).transpose()
        P = self._coefficients


        return tv.dot(Bp.dot(P))

    def Bdprime(self,t):
        Bp = np.array([
            [-6,   18, -18, 6],
            [ 6,  -12,  6, 0],
        ])

        tv = np.array([t**1, t**0]).transpose()
        P = self._coefficients


        return tv.dot(Bp.dot(P))

    def T(self,p,param=0,niter=25):
        """Get the value of t the chosen coordinate.

        Behavior is undefined if the curve is not singular in the 
        chosen first coordinate.
        """

        tl = 0.0
        tr = 1.0
        Bl = self.B(tl)
        Br = self.B(tr)

        for indx in np.arange(niter):
            tm = 0.5*(tr+tl)
            Bm = self.B(tm)

            if (Bm[param]-p)*(Bl[param]-p) > 0:
                tl = tm
                Bl = Bm
            else:
                tr = tm
                Br = Bm

        return 0.5*(tr+tl)


    def D(self,d):
        """Find the point a proportional distance d along the curve.

        The distance along the curve is not linear in t.
        The input parameter d is approximately linear with distance
        along the curve.

        Parameters
        ----------
        d : float, 0.0<=d<=1.0
            The proportional distance along the curve.

        Returns
        -------
        D : array of floats
            The coordinates of the point a proportinal distance d along
            the curve
        """

        # Find the closest distance in the lookup table
        ti = np.where(d<self.t_lookup[:,1])[0]
        if len(ti) > 0:
            # Get the associated t
            t = self.t_lookup[ti[0],0]
        else:
            t=1.0

        # Call B to get the coordinates
        return self.B(t)

    def Dprime(self,d):

        # Find the closest distance in the lookup table
        ti = np.where(d<self.t_lookup[:,1])[0]
        if len(ti) > 0:
            # Get the associated t
            t = self.t_lookup[ti[0],0]
        else:
            t=1.0

        # Call B to get the coordinates
        return self.Bprime(t)

    def Ddprime(self,d):

        # Find the closest distance in the lookup table
        ti = np.where(d<self.t_lookup[:,1])[0]
        if len(ti) > 0:
            # Get the associated t
            t = self.t_lookup[ti[0],0]
        else:
            t=1.0

        # Call B to get the coordinates
        return self.Bdprime(t)

    @property
    def t_lookup(self):
        """Build a time versus proportional distance lookup table."""

        if self._t_lookup is None or self._distances is None:
            self._t_lookup = np.zeros((len(self.distances),2))
            self._t_lookup[:,1] = self.distances/self.arc_length
            self._t_lookup[:,0] = t = np.linspace(0,1,len(self.distances))

        return self._t_lookup


    @property
    def distances(self):
        """Approximate distance along the curve at a discrete set of t values"""

        if self._distances is None:

            # Sample the curve at a bunch of points
            dist = self.B(np.linspace(0,1,30000))

            # Calculate the pair-wise distance between points
            diff = dist[:-1]-dist[1:]
            dist = np.sum(diff**2,axis=1)**0.5

            # Accumulate distances
            self._distances = np.zeros(len(dist)+1)
            for i,l in enumerate(dist,1):
                self._distances[i] = self._distances[i-1] + l

        return self._distances

    @property
    def arc_length(self):
        return self.distances[-1]

    def __getitem__(self,index):
        return self._coefficients[index]


