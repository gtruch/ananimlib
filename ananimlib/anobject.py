                    # -*- coding: utf-8 -*-
"""
AnObject classes for AnAnimLib

Created on Fri Sep  6 11:41:03 2019

@author: Fred
"""

import ananimlib as al

from PIL import Image
from xml.dom import minidom
import cairo
import numpy as np

import copy  as cp
import re

# TODO: Change where bounding box is stored.  
#    x  Let data be a generic container that render and bounding_box 
#    x  can act on.
#    x  bounding_box is an abstract property of AnObject

class AnObject():
    """Abstract Base Class for all Animation Objects.
    
    The Anobject base class defines the interface for AnObjects as used by 
    the ananimLib animation engine.  It contains the basic coordinate
    transformation information to transform between internal and external 
    coordinates based on the position, about_point, rotation, and scale 
    attributes.  
    
    In Typical usage, a Child class is defined that provides a renderer object 
    containing a render method. At render time, the animation engine will call 
    AnObject.render with a copy of the current canvas. The default render 
    method then calls renderer.render() with the data object and the canvas.  
    
    Parameters
    ----------
    data : Object
        A representation of the data to be rendered

    renderer : Object
        An object with a render method that can render the data defined by 
        the data attribute.
        Must have a render method: renderer.render(data,canvas)
    

    Attributes
    ----------

    position : Vector
        The position of the about point in external coordinates

    about_point : Vector
        The position of the about point in internal coordinates

    rotation : float
        The rotation angle between internal and external coordinates

    scale : Vector or float
        The ratio of distances in the external coordinate system to
        distances in the internal coordinate system

    clip : PolyBezier
        A PolyBezier path defining a clip region.
    """

    def __init__(self,data,renderer,clip=None):

        self.data        = data
        self.renderer    = renderer
        self.clip        = clip
        self._coordinates = al.Coordinates()


    @property
    def coordinates(self):
        return self._coordinates

    @coordinates.setter
    def coordinates(self,coordinates):
        self._coordinates = coordinates

    @property
    def position(self):
        return self._coordinates.position

    @position.setter
    def position(self,position):
        self._coordinates.position = position

    @property
    def rotation_angle(self):
        return self._coordinates.rotation_angle

    @rotation_angle.setter
    def rotation_angle(self,angle):
        self._coordinates.rotation_angle = angle

    @property
    def scale(self):
        return self._coordinates.scale

    @scale.setter
    def scale(self,scale):
        self._coordinates.scale = scale

    @property
    def transform_matrix(self):
        return self._coordinates.transform_matrix

    def internal2external(self,coords):
        """Convert internal coordinates to external coordinates."""
        return self._coordinates.internal2external(coords)

    def external2internal(self,coords):
        """Convert external coordinates to internal coordinates."""
        return self._coordinates.external2internal(coords)

    @property
    def about_point(self):
        return self._coordinates.about_point

    @about_point.setter
    def about_point(self,val):
        self._coordinates.about_point = val

    @property
    def bounding_box(self):
        """Calculate and return coordinates of the bounding box

        Returns
        -------
        bounding_box : 2x3 ndarray of floats
            Coordinates of the lower left and upper right corners
            of a box enclosing the object.
        """
        raise NotImplementedError("bounding_box must be implemented by child")

    @property
    def e_bounding_box(self):
        return self.internal2external(self.data.bounding_box)

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

    @property
    def e_center(self):
        return al.Vector(np.sum(self.e_bounding_box,axis=0)/2.0)

    @property
    def e_upper(self):
        return self.e_bounding_box[1,1]

    @property
    def e_lower(self):
        return self.e_bounding_box[0,1]

    @property
    def e_left(self):
        return self.e_bounding_box[0,0]

    @property
    def e_right(self):
        return self.e_bounding_box[1,0]

    @property
    def e_width(self):
        return self.e_right - self.e_left

    def about_center(self):
        """Move the about point to the center of the anobject"""
        self._coordinates.about_point = self.center

    def about_lower(self):
        """Move the y-coord of the about point to the lower bound."""
        self._coordinates.about_point = [self._coordinates.about_point.x,
                                         self.lower]
    def about_upper(self):
        """Move the y-coord of the about point to the upper bound."""
        self._coordinates.about_point = [self._coordinates.about_point.x,
                                         self.upper]

    def about_left(self):
        """Move the x-coord of the about point to the left bound."""
        self._coordinates.about_point = [self.left,
                                         self._coordinates.about_point.y]

    def about_right(self):
        """Move the x-coord of the about point to the right bound."""
        self._coordinates.about_point = [self.right,
                                         self._coordinates.about_point.y]
    def render(self,canvas):
        """Render the data object onto the requested canvas."""
        self.renderer.render(self,canvas)


class BezierAnObject(AnObject):
    """An Animation Object containing a Bezier path and a Pen to draw it.

    BezierAnObject will render an arbitrary open or closed path 
    defined by a PolyBezier curve using a BezierRender object as the renderer.  
    BezierRender renders the path according to the attributes of Pen object.  
    
    Parameters
    ----------
    path : PolyBezier
        A Poly Bezier curve representing a path to be rendered

    pen : Pen
        A pen representing the appearance of the path.

    """


    def __init__(self,path=None,pen=None):

        if path is None:
            path = al.PolyBezier()

        super().__init__(path,al.BezierRender(pen))
        
    def connect_linear(self,points):
        self.data.connect_linear(points)

    def connect_smooth(self,points):
        self.data.connect_smooth(points)
        
    def clear(self):
        self.data = al.PolyBezier()

    @property
    def bounding_box(self):
        return self.data.bounding_box
    
    @property
    def pen(self):
        return self.renderer.pen
    
    @pen.setter
    def pen(self, val):
        self.renderer.pen = val

    @property
    def stroke_opacity(self):
        return self.renderer.pen.stroke_opacity

    @stroke_opacity.setter
    def stroke_opacity(self, opacity):
        self.renderer.pen.stroke_opacity = opacity

    @property
    def stroke_color(self):
        return self.renderer.pen.stroke_color

    @stroke_color.setter
    def stroke_color(self, color):
        self.renderer.pen.stroke_color = color

    @property
    def stroke_width(self):
        return self.renderer.pen.stroke_width

    @stroke_width.setter
    def stroke_width(self, width):
        self.renderer.pen.stroke_width = width

    @property
    def fill_opacity(self):
        return self.renderer.pen.fill_opacity

    @fill_opacity.setter
    def fill_opacity(self, opacity):
        self.renderer.pen.fill_opacity = opacity

    @property
    def fill_color(self):
        return self.renderer.pen.fill_color

    @fill_color.setter
    def fill_color(self, color):
        self.renderer.pen.fill_color = color


class ImageAnObject(AnObject):
    """Animation Object containing a bitmapped image

    Parameters
    ----------
    filename : str
        The name of the image file

    scale_height : optional, float
        The number of Scene Units that the the full height of the image
        should occupy.  The aspect ratio of the image will be maintained.
        default = 1.0, meaning the image will be 1 Scene Unit tall.
        
        
    Attributes
    ----------
    """

    def __init__(self,filename,scale_height=None):

        # Open the image file and pack it into a container
        image = Image.open(filename).convert('RGBA')
        
        self.pw, self.ph = image.size
        
        self.image = np.array(image)
        self._opacity = 1.0
        self._alpha = cp.copy(self.image[:,:,3])

        data = ImageContainer(
            cairo.ImageSurface.create_for_data(
                bytearray(image.tobytes('raw', 'BGRa')),
                cairo.FORMAT_ARGB32,
                self.pw,self.ph))

        # Initialize the AnObject with the container and renderer
        super().__init__(data,al.ImageRender())

        # Set the scale, position, and about point
        self.scale_height = scale_height
        self.about_center()
        self.position = [0.0,0.0]
        
        self.invert()

    @property     
    def bounding_box(self):
        return self.data.bounding_box

    def invert(self):
        """Invert the image, top to bottom"""
        self.image = np.array(np.flip(self.image,axis=0))
        self.data = ImageContainer(
            cairo.ImageSurface.create_for_data(
                self.image,
                cairo.FORMAT_ARGB32,
                self.pw,self.ph))

    def mirror(self):
        """Flip image left to right"""
        self.image = np.array(np.flip(self.image,axis=1))
        self.data = ImageContainer(
            cairo.ImageSurface.create_for_data(
                self.image,
                cairo.FORMAT_ARGB32,
                self.pw,self.ph))

    @property
    def opacity(self):
        return self._opacity

    @opacity.setter
    def opacity(self,val):
        self._opacity=val
        self.image[:,:,3] = val*self._alpha

    def set_scale(self,dpi):
        """Set the scale prior to rendering"""
        self._coordinates.scale = self.scale_height/dpi


    def render(self,camera):

#        dpi = camera.pixelsPerFrame[1]/camera.sceneUnitsPerFrame[1]

#        self.set_scale(dpi)

        super().render(camera)

class FreetypeAnObject(AnObject):
    """Freetype text rendered as an image.  Experimental"""

    def __init__(self,text):
        """Use freetype to build an image of the text string."""

        # Use Freetype to render some text as a bitmap
#        face = ft.Face("C:/Windows/Fonts/arial.ttf")
        face = None
        face.set_char_size( 48*64 )
        face.load_char('S')
        bitmap = face.glyph.bitmap

        # Convert the bitmap to a numpy array
        pixels = np.asarray(bitmap.buffer,dtype=np.uint8)
        pix = pixels.reshape(bitmap.rows,bitmap.width)

        im = Image.fromarray(pix).convert('RGBA')

        # Pack the numpy array into a cairo surface
        data = ImageContainer(
            cairo.ImageSurface.create_for_data(
                np.array(np.flip(im,axis=0)),
                cairo.FORMAT_ARGB32,
                bitmap.width,
                bitmap.rows))

        super().__init__(data,al.ImageRender())

        # Set the scale and position
        self.scale_height = 1.0
        self.about_center()
        self.position=[0.0,0.0]


    def render(self,camera):
        """Set the scale prior to rendering"""
        scale = (camera.sceneUnitsPerFrame[1]/camera.pixelsPerFrame[1]*
                                                          self.scale_height)
        self.scale = scale
        super().render(camera)


class ImageContainer():
    """Container for bitmapped images represented by a cairo surface"""

    def __init__(self,surface):
        self.surface = surface
        self.bounding_box = np.array([
            [0,0],[surface.get_width(),surface.get_height()]
        ])


class CompositeAnObject(AnObject):
    """Animation Object constructed from multiple sub-anobjects.
    
    Allows sub-anobjects (any of which can also be a 
    CompositeAnObject) to be grouped into a single unit.  All position, scale, 
    and rotations on the CompositeAnObject will effect all AnObjects in the 
    composite such that their individual scales, positions, and rotations 
    relative to one another will remain fixed.  
    
    Sub-anobjects can be manipulated through standard array indexing syntax.  If 
    a sub-anobject is a CompositeAnObject, its members can be access by passing a 
    tuple as the index.  
    """

    def __init__(self,anobjects=None,names=None):

        self.clear()

        # self.anobjects = {}      # a dictionary with the anobjects.
        # self.keys = []           # a simple list of keys to remember the 
        #                          # insertion order (z-order)
        # self.key_lookup = {}     # Look up the key using the anobject's object id
        
        if anobjects is not None:

            # If no names were passed, use the object id
            if names is None:
                names = [str(id(mob)) for mob in anobjects]

            for mob,name in zip(anobjects,names):
                self.add_anobject(mob,name)

        super().__init__(self.anobjects, al.CompositeRender())

    def clear(self):
        self.anobjects = {}      # a dictionary with the anobjects.
        self.keys = []           # a simple list of keys to remember the 
                                 # insertion order (z-order)
        self.key_lookup = {}     # Look up the key using the anobject's object id

    def add_anobject(self, anobject, key=None, path=None, update_transform=True):
        """Add an AnObject to the composite

        Parameters
        ----------
        anobject : AnObject
            An instance of a class derived from AnObject

        name : str
            The name of the anobject for retrieval and manipulation
            
        path : iterable
            An iterable of forward links indicating where in the Composite tree 
            to place this AnObject.
            
        update_transform : optional boolean
            default = True
            The coordinates of a anobject (the position, scale, and rotation) 
            are representd by an affine transformation which is applied just
            prior to rendering.  A CompositeAnObject has its own transformation 
            which is applied before rendering any sub-anobjects.  
        
            When update_transform is True, the new anobject's coordinates 
            (position, scale, and rotation) are modified by applying the 
            inverse of the CompositeAnObject's transformation effectively 
            undoing it so that its final rendered position on the canvas is the 
            same as it would have been before the call to add_anobject.  
            This modification happens only once at the time that add_anobject 
            is called. 
            
            When false, the added anobject's coordinates will NOT be modified 
            which, depending on state of the CompositeAnObject's transformation, 
            will could cause its rendered appearance to change.  
        """
                                   
        # If there is no path, add the AnObject to this Composite.
        if path is None: 
            
            # If the input anobject is a bare anobject, put it in a list
            if isinstance(anobject, al.AnObject): 
                anobjects = [anobject]
            else:
                anobjects = anobject
                
            # Manage the key (or keys)
            keys = []
            if key is None:
                keys = [str(id(an)) for an in anobjects]
            elif len(anobjects) == 1:
                keys = [key]
            else: 
                keys = key
            
            # Make sure that there are the same number of keys as AnObjects
            if len(keys) < len(anobjects):
                raise ValueError("Number of keys must match number of AnObjects")

            # Run the list and pack them in
            for anobject, key in zip(anobjects,keys):
                
                # Store the anobject and its key in all the right places.
                self.anobjects[key] = anobject      # Main dictionary
                self.key_lookup[anobject] = key     # Reverse dictionary
                self.keys.append(key)               # Key list to maintain 
                                                    #          insertion order
                
        elif len(path) == 0:                      # ignore empty path
            self.add(anobject,key)
        else:
            
            # Recursively walk the path
            next_target = self.get(path[0])       # Follow forward link
            next_path   = path[1:]                # Split the path
            
            if len(next_path) == 0:               # Set empty path to None
                next_path = None
                                
            # Call the add method of the next target.
            next_target.add(anobject, key, next_path)
            
    def get_anobject(self,key):
        """Get a reference to an AnObject that's in the container
        """
             
        # Passed key is actually an AnObject.  Attempt to look up the key.
        if isinstance(key,al.AnObject):
            
            if key in self.key_lookup:
                key = self.key_lookup[key]
            else:                 
                raise KeyError("AnObject reference passed as a key but"
                                 " that AnObject is not in this Composite.")

        if isinstance(key,str):
            
            # Passed key is a string, let's see what we have on file...
            if key in self.anobjects.keys():
                return self.anobjects[key]
            else:
                raise ValueError(f"No AnObject listed with key='{key}'")
        
        elif len(key) > 1: 
            return self.get_anobject(key[0]).get_anobject(key[1:])
        else:
            return self.get_anobject(key[0])
            
    @property
    def bounding_box(self):
        """Get the coordinates of the bounding box

        Returns
        -------
        An 2x3 ndarray containing the lower left (row 1) and the
        upper right (row 2) of the bounding box.
        """

        if len(self.anobjects) == 0:
            return np.zeros((2,3))

        box = []
        for mob in self.anobjects.values():
            bb = mob.bounding_box
            bb = mob.internal2external(bb)
            box.append(mob.internal2external(mob.bounding_box))

        box = np.array(box)
        box = np.concatenate((box[:,0,:],box[:,1,:]))

        return np.array([box.min(axis=0),box.max(axis=0)])

    # def add_anobject(self,anobject,name=None,preserve_transform=True):
    #     """Add an animation object to the collection

    #     Parameters
    #     ----------
    #     anobject : AnObject
    #         An instance of a class derived from AnObject

    #     name : str
    #         The name of the anobject for retrieval and manipulation
            
    #     preserve_transform : optional boolean
    #         The coordinates of a anobject (the position, scale, and rotation) 
    #         are representd by an affine transformation which is applied just
    #         prior to rendering.  A CompositeAnObject has its own transformation 
    #         which is applied before rendering any sub-anobjects.  
        
    #         When preserve_transform is True, the added anobject's coordinates 
    #         (position, scale, and rotation) are modified by applying the 
    #         inverse of the CompositeAnObject's transformation effectively 
    #         undoing it so that its final rendered position on the canvas is the 
    #         same as it would have been before the call to add_anobject.  
    #         This modification happens only once at the time that add_anobject 
    #         is called. 
            
    #         When false, the added anobject's coordinates will NOT be modified 
    #         which, depending on state of the CompositeAnObject's transformation, 
    #         will could cause its rendered appearance to change.  
    #     """

    #     if preserve_transform:
    #         # Set position to internal coordinates
    #         anobject.position = self.external2internal(anobject.position)

    #         # Change the scale to counter the composite scale
    #         anobject.scale = anobject.scale*self.scale**-1

    #     # # Change the rotation to counter the composite rotation
    #     # anobject.rotation_angle = anobject.rotation_angle self.rotation_angle*-1

    #     self.data.add_anobject(anobject,name)

    # def remove_anobject(self,name):
    #     """Remove a anobject from the composite.  Synonym for pop."""
        
    #     self.data.pop(name)
        

    # def clear(self):
    #     """Remove all anobjects from the composite"""
        
    #     self.data.clear()

    # def get_anobject(self,name):
    #     """Fetch a anobject from the group.  Synonym for __getitem__

    #     Parameters
    #     ----------
    #     name : str
    #         The name of the anobject
    #     """

    #     return self[name]
    
    def set_attributes(self,attribute,value,keys=None):
        """Set the same attribute on each of the of selected sub-anobjects 
        
        Parameters
        ----------
        attribute : string
            The name of the attribute 
            
        value 
            The desired attribute value
            
        keys : optional, iterable of strings
            The keys of the anobjects whose attribute should be set.
            default = all contained anobjects.  
        """

        if keys is None:
            keys = self.data.keys

        for key in keys:
            mb = self.data.get_anobject(key)
            if hasattr(mb,attribute):
                setattr(mb,attribute,value)

    def group(self,indices,name):
        """Place a set of anobjects into composite under a single key

        Parameters
        ----------
        indices : slice
            An array of the indices (ints or keys) to add to the new
            composite

        name : string
            The key under which to store the new composite anobject
        """

        # Create a new instance of this composite type
        new_mob = self.__class__()

        # Get the old keys
        old_keys = []
        for i in indices:

            # Get the key
            if i in self.data.keys:
                old_keys.append(i)
            else:
                old_keys.append(self.data.keys[i])


        # Group the anobjects
        for key in old_keys:

            # Remove the anobject and put it in the new composite
            mob = self.data.pop(key)
            new_mob.add_anobject(mob,key)

        # Add the new composite to current composite
        self.add_anobject(new_mob,name,preserve_transform=False)
        new_mob.about_center()



    # def __getitem__(self,index):
        
        
    #     if isinstance(index,slice):
    #         ret = cp.deepcopy(self)
    #         ret.data = self.data[index]
    #         return ret
    #     elif isinstance(index,list) or isinstance(index,tuple):
    #         if len(index) > 1:
    #             return self[index[0]][index[1:]]
    #         else:
    #             return self[index[0]]
    #     else:
    #         return self.data[index]

    # def __setitem__(self,index,value):
    #     pass
        

    # def __len__(self):
    #     return len(self.data)


# class AnObjectContainer():
#     """A container to hold a collection of anobjects
    
#     This is where the Animation Object data structure lives."""

#     def __init__(self,anobjects=None,names=None):
#         super().__init__()

        
#         self.anobjects = {}      # a dictionary with the anobjects.
#         self.keys = []          # a simple list of keys to remember the 
#                                 # insertion order (z-order)
#         self.key_lookup = {}    # Look up the key using the anobject's object id
        
#         if anobjects is not None:

#             # If no names were passed, use the object id
#             if names is None:
#                 names = [str(id(mob)) for mob in anobjects]

#             for mob,name in zip(anobjects,names):
#                 self.add_anobject(mob,name)


#     def add_anobject(self,anobject,key=None):
#         """Add a anobject to the collection

#         Parameters
#         ----------
#         anobject : AnObject
#             An instance of a class derived from AnObject

#         key : optional str 
#             A key to use for later anobject retrieval when the anobject itself 
#             is unavailable.
#         """
        
#         # Fetch the object id
#         obj_id = str(id(anobject))
        
#         # If no key is given, use the object id as a key
#         if key is None:
#             key = obj_id
        
#         # Store the key in the keys list
#         self.keys.append(key)
        
#         # Store the object id/key pair for key lookup 
#         self.key_lookup[obj_id] = key
        
#         # Store the actual anobject
#         self.anobjects[key] = anobject


#     def get_anobject(self,key):
#         """Fetch a anobject from the group.  synonym for __getitem__

#         Parameters
#         ----------
#         key : str or anobject
#             The name of the anobject or the anobject itself
#         """
#         return self[key]


#     @property
#     def bounding_box(self):
#         """Get the coordinates of the bounding box

#         Returns
#         -------
#         An 2x3 ndarray containing the lower left (row 1) and the
#         upper right (row 2) of the bounding box.
#         """

#         if len(self.anobjects) == 0:
#             return np.zeros((2,3))

#         box = []
#         for mob in self.anobjects.values():
#             bb = mob.bounding_box
#             bb = mob.internal2external(bb)
#             box.append(mob.internal2external(mob.bounding_box))

#         box = np.array(box)
#         box = np.concatenate((box[:,0,:],box[:,1,:]))

#         return np.array([box.min(axis=0),box.max(axis=0)])


#     def pop(self,key):

#         if key in self.keys:
#             self.keys.remove(key)
#             return self.anobjects.pop(key)
#         else:
#             if key[0] in self.keys:
#                 if len(key) == 1:
#                     return self.pop(key[0])
#                 else:
#                     return self.anobjects[key[0]].remove_anobject(key[1:])

#     def clear(self):
#         self.keys.clear()
#         self.anobjects.clear()

#     def move_to_bottom(self,key):
#         """Move requested anobject to the front of the keys list.

#         This effectively puts it at the bottom of the z-order as it gets
#         rendered first"""
#         if key in self.keys:
#             i = self.keys.index(key)
#             self.keys.insert(0,self.keys.pop(i))

#     def bring_to_top(self,key):
#         """Move requested anobject to the end of the keys list.

#         This effectively puts it at top of the z-order as it gets rendered last
#         """
#         if key in self.keys:
#             i = self.keys.index(key)
#             self.keys.append(self.keys.pop(i))

#     def __iter__(self):
#         for k in self.keys:
#             yield self.anobjects[k]

#     def __getitem__(self,index):
#         """Retrieve an anobject
        
#         Parameters
#         ----------
#         index : slice, string, str or anobject
        
#         """
        

#         # Slice it up and return an AnObjectContainer
#         if isinstance(index,slice):
#             items = [self.anobjects[k] for k in self.keys[index]]
#             return AnObjectContainer(items,self.keys[index])

#         # Retrieve by integer index
#         if isinstance(index,int):
#             key = self.keys[index]

#         # Retrieve by object id
#         elif isinstance(index,AnObject):
            
#             # It's an AnObject.  Is it in our index?
#             obj_id = str(id(index))   # We store the by id
            
#             try : 
#                 key = self.key_lookup[obj_id]
#             except KeyError :
#                 err = f"object of type {index.__class__} with id {obj_id} isn't here man."
#                 raise KeyError(err)
            
#         # index must be the key
#         else: 
#             key = index

#         # Fetch and return!
#         return self.anobjects[key]



#     def __len__(self):
#         return len(self.keys)

class SVGAnObject(CompositeAnObject):
    """Parse SVG file into a CompositeAnObject

    Extremely limited SVG processing.  
    Used for reading latex output from an svg file created by dvisvgm  
    (See TexAnObject)
    """

    def __init__(self,file=None,pen=None,rescale=1.0):
        """Process the svg file

        Parameters
        ----------
        file : str
            The name of the svg file to process

        pen : optional Pen
            The pen to use for rendering the paths

        rescale : optional float
            Used to rescale the coordinates before building the Bezier curves.
            default = 1.0, 1:1 scaling

        """
        super().__init__()



        # Keep track of transformations from the SVG
        self.coord = al.Coordinates()

        self.rescale = rescale
        self.pen=pen

        # Stack for saving nested transformations
        self.stack = []

        # Dictionary to hold SVG definitions
        self.defs = {}

        # Open the file with minidom and process it.
        if file is None:
            return

        doc = minidom.parse(file)
        self._process_doc(doc)


    def _process_doc(self,node):
        """Recursive SVG processor

        Parameters
        ----------
        node : minidom node
            The current node from the minidom tree
        """

        # Push a copy of the current coordinate transform
        self.stack.append(cp.deepcopy(self.coord))

        # Process only nodes that I'm looking for and ignore the rest
        if node.nodeName == 'svg':
            # Base tag for SVG document fragments
            # Can be used to set up a viewport, but currently
            # ignored
            pass    # Do nothing for now.

        elif node.nodeName == 'g':
            # Grouping command.  The coordinate system could be
            # modified here by a transform
            if node.hasAttribute('transform'):
                self.apply_transform(node.getAttribute('transform'))
            pass

        elif node.nodeName == 'defs':
            # Build the definitions dictionary
            self.build_defs(node.childNodes)
            node.childNodes = []

        elif node.nodeName == 'use':

            # 'use' updates the relative position of the coordinate system
            # Take the offsets and use them
            raw = al.Vector(float(node.getAttribute('x')),
                             float(node.getAttribute('y'))*-1.0)

            raw1 = self.coord.external2internal(raw)
            raw2 = self.coord.internal2external(raw)
            raw3 = raw*self.coord.scale*self.rescale

            self.coord.position += raw3

            # Process the original svg element from the dictionary
            self._process_doc(self.defs[node.getAttribute('xlink:href')[1:]])

        elif node.nodeName == 'path':

            # Convert the path into a PolyBezier object
            path = al.SVGPolyBezier(node.getAttribute('d'))
            path.points = path.points*self.rescale

            # Create a new BezierAnObject and update its coordinate transform
            obj = BezierAnObject(path=path,pen=cp.deepcopy(self.pen))
            obj.coordinates = cp.deepcopy(self.coord)

            # Add this new anobject to the composite
            self.add_anobject(obj)

        elif node.nodeName == 'rect':
            # Create a rectangle

            path = al.PolyBezier()
            x = float(node.getAttribute('x'))*self.rescale
            y = float(node.getAttribute('y'))*-1*self.rescale
            height = float(node.getAttribute('height'))*self.rescale
            width = float(node.getAttribute('width'))*self.rescale
            path.connectLinear([[0.0,0.0],
                                [0.0,height],
                                [width,height],
                                [width,0.0],
                                [0.0,0.0]])

            obj = BezierAnObject(path=path,pen=cp.deepcopy(self.pen))
            obj.coordinates = cp.deepcopy(self.coord)
            obj.position = [x,y]

            self.add_anobject(obj)

        else:
            pass

        # Process children recursively
        if len(node.childNodes) > 0:
            for child in node.childNodes:
                self._process_doc(child)

        # Restore the coordinate transform from the previous level
        self.coord = self.stack.pop()

    def apply_transform(self, trans_attr):
        """Apply the transform matrix from a transform attribute"""

        # Fetch the transform string
        data = trans_attr

        # Is it a matrix?
        if data.startswith("matrix"):

            # Extract the components of the transform matrix
            reg = re.compile(r'[0-9]+\.[0-9]+|[0-9]+')
            components = reg.findall(data)

            # Convert into floats
            components = np.array([float(c) for c in components]).reshape(3,2)
            components = components.transpose()

            matrix = np.diag([1.0,1.0,1.0])
            matrix[:2,:] = components
            matrix[:2,2] *= self.rescale
            matrix[1,2]  *= -1

            # Create a new coordinate object and combine it with the existing
            # coordinates
            new_coords = al.Coordinates()
            new_coords.transform_matrix = matrix
            self.coord = self.coord*new_coords


    def build_defs(self,nodelist):
        # Process a block of svg definitions

        for node in nodelist:
            if isinstance(node, minidom.Element) and node.hasAttribute('id'):
                self.defs[node.getAttribute('id')] = node



