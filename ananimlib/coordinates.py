# -*- coding: utf-8 -*-
"""
Affine transformations

Created on Wed Dec 11 15:19:42 2019

@author: G.Ruch
"""

import math
import numpy as np
import scipy.linalg

class Coordinates():
    """Handle Affine transformations between coordinate spaces.

    The transformation represents a Rotation, Scale and Translation around an
    about point.

    Attributes
    ----------
    position : Vector
        Position of the about point in the external coordinate space A

    about_point : Vector
        Position of the about point in the internal coordinate space

    scale : Vector
        The ratio of distances in the external space to distances in the
        internal space

    rotation_angle : float
        The rotation angle of space Y with respect to space X

    transform_matrix : read only 3x3 ndarray of floats
        The affine transformation matrix based on Xposition, Yposition,
        scale, and rotation_angle
    """

    def __init__(self,position=None, about_point=None,
                      rotation_angle=None, scale=None):

        self._position = (Vector(0.0,0.0,0.0) if   (position is None)
                          else position)

        self._scale = np.ones(3) if (scale is None) else scale

        self._rotation_angle = (0.0 if   (rotation_angle is None)
                                else rotation_angle)

        self._about_point = (Vector(0.0,0.0,0.0) if (about_point is None)
                            else about_point)

        self._calc_matrix()

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self,val):
        self._position = Vector(val)
        self._calc_matrix()

    @property
    def about_point(self):
        return self._about_point

    @about_point.setter
    def about_point(self,val):
        self._about_point = Vector(val)

        # Update the position so the transform matrix stays the same.
        rot = Affine2d(rotation=self.rotation_angle)
        ap  = Affine2d(offset=-self._about_point)

        pos = self._matrix*scipy.linalg.inv(rot*ap)
        self.position     = Vectors([0.0,0.0]).apply_affine_transform(pos)

    @property
    def rotation_angle(self):
        return self._rotation_angle

    @rotation_angle.setter
    def rotation_angle(self,angle):
        self._rotation_angle = angle
        self._calc_matrix()

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self,val):
        val = Vector(val)

        # Make sure the scale vector doesn't have zeros on the diagonal
        if val.y == 0:
            val.y = val.x
        if val.z == 0:
            val.z = 1.0

        self._scale = Vector(val)


        self._calc_matrix()

    @property
    def transform_matrix(self):
        return self._matrix

    @transform_matrix.setter
    def transform_matrix(self,matrix):

        # Decompose the transform matrix into offset, rotation, and scale
        # Leave the about point at zero
        self.about_point = [0,0]
        self.position = matrix[:2,2]
        self.scale = np.sqrt([np.sign(matrix[0,0])*np.sum(matrix[0,:2]**2),
                              np.sign(matrix[1,1])*np.sum(matrix[1,:2]**2)])
        self.rotation_angle = np.arctan(matrix[0,1]/matrix[1,1])

    def external2internal(self,mcoords):
        """Convert external coordinates to internal coordinates."""
        fmcoords = Vectors(mcoords)
        return fmcoords.apply_affine_transform(scipy.linalg.inv(self._matrix))

    def internal2external(self,scoords):
        """Convert internal coordinates to external coordinates."""
        fscoords = Vectors(scoords)
        return fscoords.apply_affine_transform(self._matrix)

    def _calc_matrix(self):
        rot = Affine2d(rotation=self.rotation_angle)
        sc  = Affine2d(scale=self.scale)
        pos = Affine2d(offset=self.position)
        ap  = Affine2d(offset=-self.about_point)
        self._matrix = pos*sc*rot*ap

    def __mul__(self,other):
        """Multiply the transformation matrices"""

        # Update the rotation, scale, position, and about point
        new_position = self.position + other.position


        new_rotation_angle = self.rotation_angle + other.rotation_angle
        new_scale = self.scale*other.scale

        return Coordinates(position=new_position,
                           about_point = self.about_point,
                           rotation_angle=new_rotation_angle,
                           scale=new_scale)


class Affine2d(np.ndarray):
    """Matrix representing a 2d affine transformation."""

    def __new__(cls, offset        = None,
                     scale         = None,
                     rotation      = 0.0):

        """Let's get set up!

        ndarray uses __new__ rather than __init__.
        See numpy docs for further information

        Start with the identity matrix.
        """

        if offset is None:
            offset = np.array([0,0,1])
        else:
            offset = np.array([offset[0],offset[1],1.])

        if scale is None:
            scale = np.array([1.,1.,1.])
        elif scale[1] == 0:
            scale = np.array([scale[0],scale[0],1.0])
        else:
            scale = np.array([scale[0],scale[1],1.0])

        # Apply rotation
        data = np.array([
            [np.cos(rotation),-np.sin(rotation),   0],
            [np.sin(rotation), np.cos(rotation),   0],
            [               0,                0, 1.0]
        ])

        # Apply scale
        data[range(3),range(3)] = np.diag(data)*scale

        # Apply offset
        data[:2,2] = offset[:2]
#        data = data.transpose()

        return np.asarray(data).view(cls)

    def __mul__(self,other):
        return self.dot(other)


class Vectors(np.ndarray):
    """Flexible ndarray to represent a set of 3D vectors."""

    def __new__(cls,data):
        """Let's get set up.

        ndarray uses __new__ rather than __init__.
        See numpy docs for further information

        Parameters
        ----------
        data : iterable of floats
            Matrix of cartesian components
            n is the number of vectors in the set.
            rows 0,1,2 are the x,y,z components respectively

            If there are less than 3, remaining columns will be filled
            with zeros.
        """
        shape = np.array(data).shape

        if len(shape)==1:
            _data = np.array(Vector(data))
        else:
            _data = np.zeros((len(data),3))

            for row,datum in enumerate(data):
                _data[row,:] = Vector(datum)

        return np.asarray(_data).view(cls)

    def get_vector(self,index):
        """Get a vector"""
        return Vector(self[index])

    def apply_affine_transform(self,transform_matrix):
        """Apply an affine transformation

        Parameters
        ----------
        transform_matrix : 3x3 or 4x4 ndarray of floats
            The transform matrix.
            If 3x3:
            -    A 2d transformation is applied and
            -    z-coordinates are maintained
            If 4x4:
            -    A 3d transformation is applied
        """

        # Get the shape of the transform matrix
        trans_dims,_   = transform_matrix.shape

        if len(self.shape) == 1:
            num_vecs = 1
            vec = self[None,:]
        else:
            num_vecs,_  = self.shape
            vec = self[:]

        # Create the augmented coordinate matrix
        aug = np.ones((num_vecs,trans_dims))
        aug[:,:-1] = vec[:,:(trans_dims-1)]

        # Perform the transform
        aug = transform_matrix.dot(aug.transpose()).transpose()

        if trans_dims == 3:
            # Put z components back
            aug[:,2] = vec[:,2]
        else:
            # Strip augmented column
            aug = aug[:,:-1]


        if num_vecs == 1:
            return Vector(aug[0])
        else:
            return Vectors(aug)


class Vector(np.ndarray):
    """Three dimensional vector to represent a point in 3-space

    Attributes
    ----------
    x,y,z : float
        cartesian components

    r,theta,phi : float
        Spherical components
    """

    def __new__(cls,x,y=0.0,z=0.0):
        """Let's get set up!

        ndarray uses __new__ rather than __init__.
        See numpy docs for further information

        Parameters
        ----------
        x,y,z : float
            Cartesian components

            If x is an iterable, x,y,and z will be set with its contents and
            named parameters y and z will be ignored. If the iterable in x
            contains fewer than three elements, the remaining elements will
            be filled with zeros.

            If x is not iterable, x, y, and z will be taken from the named
            parameters where y and z default to zero if not specified.
        """

        if isinstance(x,np.ndarray) and len(x) == 3:
            data = x   # Go fast if this is a numpy array
        else:

            try:

                # x is iterable. Use the data found in x
                d = np.array([float(d) for d in x])

                if len(d) > 3:
                    raise ValueError("Vectors can be initialized with " +
                                     "a maximum of 3 components")

                data = np.zeros(3)
                data[:len(d)] = d

            except TypeError:

                # x is not iterable.  Take data from named parameters
                data = np.array([float(x),float(y),float(z)])

        return np.asarray(data).view(cls)

    @classmethod
    def as_ndarray(cls,data):
        return np.asarray(data).view(cls)

    @classmethod
    def asSpherical(cls,r,theta,phi=np.pi/2):
        """Initialize with spherical coordinates

        Parameters
        ----------
        r, theta : float
            The magnitude and azimuthal angle (in radians) respectively

        phi : optional, float
            The polar angle in radians (default = pi/2)
        """

        x,y,z = cls._sphericalToCartesian(r,theta,phi)
        return cls(x,y,z)

    @property
    def x(self):
        return self[0]

    @x.setter
    def x(self, value):
        self[0] = value

    @property
    def y(self):
        return self[1]

    @y.setter
    def y(self, value):
        self[1] = value

    @property
    def z(self):
        return self[2]

    @z.setter
    def z(self, value):
        self[2] = value

    @property
    def r(self):
#        return float(np.sqrt(np.sum(self*self)))
        return float(np.sqrt(self[0]**2+self[1]**2+self[2]**2))

    @property
    def theta(self):
        return math.atan2(self.y,self.x)

    @property
    def phi(self):
        return math.atan2(math.sqrt(self.x**2+self.y**2),self.z)

    @r.setter
    def r(self,r):
        x,y,z = self._sphericalToCartesian(r,self.theta,self.phi)
        self.x = x
        self.y = y
        self.z = z

    @theta.setter
    def theta(self,theta):
        x,y,z = self._sphericalToCartesian(self.r,theta,self.phi)
        self.x = x
        self.y = y
        self.z = z

    @phi.setter
    def phi(self,phi):
        x,y,z = self._sphericalToCartesian(self.r,self.theta,phi)
        self.x = x
        self.y = y
        self.z = z

    @property
    def mag(self):
        return float(np.sqrt(np.sum(self*self)))

    @mag.setter
    def mag(self, magnitude):
        x,y,z = self._sphericalToCartesian(magnitude,self.theta,self.phi)
        self.x = x
        self.y = y
        self.z = z

    @property
    def unit(self):
        m = self.mag
        return Vector(self.x/m,self.y/m,self.z/m)
    
    @staticmethod
    def _sphericalToCartesian(r,theta,phi):
        """Convert sperical coordinates to cartesian

        Parameters
        ----------
        r, theta, phi : float
            The magnitude, azimuthal angle, and polar angle respectively

        Returns
        -------
        x, y, x : float
            The cartesian x, y, and z components respectively
        """

        return (r*math.sin(phi)*math.cos(theta),
                r*math.sin(phi)*math.sin(theta),
                r*math.cos(phi))

    def __sub__(self,other):
        return super().__sub__(Vector(other))
    
    def __add__(self,other):
        return super().__add__(Vector(other))
    

