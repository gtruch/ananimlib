# Coordinate tranformations
from .coordinates import Coordinates, Vector, Vectors

# Transfer Functions for Instruction timing
from .transfer_funcs import linear, smooth, there_and_back 

# The animation engine
from .ananim import AnEngine

# Base animation objects
from .anobject import AnObject, BezierAnObject, ImageAnObject, \
                      CompositeAnObject, SVGAnObject
                    
from .scene import Scene

# Commonly used animation objects
from .common_anobs import CrossHair, Grid, Circle, Dot, Arc, Arrow, \
                         DoubleArrow, ArrowHead, Rectangle, Line
                       
# LaTex related animation objects
from .tex_anobject import Text, TexMath, Number, TextBox

# Plotting animation objects
from .plot_anobs import CoordAxis, CoordGrid

# Instruction data structures
from .instruction import Instruction, InstructionTree

# Core Instructions upon which most other instructions are based. 
from .core_instructions import RunParallel, RunSequential, \
                               SetAttribute, SlideAttribute, Timing

# Basic set of instructions
from .basic_instructions import AddAnObject, RemoveAnObject, Move, MoveTo, \
                                Rotate, Scale, AboutCenter, AboutLeft, \
                                AboutRight, AboutUpper, AboutLower, \
                                AdjustAboutPoint, SetAboutPoint, Swap, Draw, \
                                DrawText, MoveCamera, ZoomCamera, Emphasize, \
                                FollowPath, AlignWithPath, GrowArrow, Wait

# Search algorithms
from .search import Bisect, Newton

# Bezier classes for Bezier Curve manipulation
from .bezier import BezierCurve, PolyBezier, SVGPolyBezier

# Rendering classes
from .render import BezierRender, CompositeRender, ImageRender, CairoRender, Pen               

# The camera 
from .camera import Camera

# Backend to manipulate the video stream
from .backend import Backend

# defaults for control of the renderer
_defaults = {
    'width'      : 16,      
    'ar'         : 16/9, 
    'frame_rate' : 60, 
    'DPI'        : 120,
    'tex_dir'    : './tex'
}

# Global default pen    
_default_pen = None

# Instantiate a default animation engine and provide the Animate method
engine = AnEngine()

Animate = engine.run            # Animate is just an alias for AnEngine.run
play_movie = engine.play_movie

# Provide access to frame rate and frame size parameters
#frame_rate = get_dict_attr()






























