AnAnimLib API Reference
=======================

Animate 
-------

Consider the following script.

.. literalinclude:: ./code/quickstart_ex1.py
  :start-after: # START
  :end-before: # END
  :linenos:


On line 3, we call *al.Animate* to render our animation, but where does *Animate*
come from?  On import, *AnAnimLib* instantiates an :ref:`AnEngine` object labeled
*engine* into the *AnAnimLib* namespace.  Then, the :ref:`run` method of *engine* is
mapped to *Animate*.  In otherwords, line 3 of the script above could be
replaced by

.. code::

   al.engine.run(

but al.Animate looks better in the code (imho) and more clearly represents what
we are actually doing.  The name *run* refers to the fact that we are running
the main loop, so it's nice to have that reminder when we dig down to the next
layer.  

.. _AnEngine:

AnEngine
--------

.. autoclass:: ananimlib.ananim.AnEngine
   :members: 

Simple Animation Objects (AnObjects)
------------------------------------

Arc
^^^

.. autoclass:: ananimlib.Arc
   :members:

Arrow
^^^^^

.. autoclass:: ananimlib.Arrow
   :members:

ArrowHead
^^^^^^^^^

.. autoclass:: ananimlib.ArrowHead
   :members:

Circle
^^^^^^

.. autoclass:: ananimlib.Circle
   :members:

CrossHair
^^^^^^^^^

.. autoclass:: ananimlib.CrossHair
   :members:

Dot
^^^

.. autoclass:: ananimlib.Dot
   :members:

DoubleArrow
^^^^^^^^^^^

.. autoclass:: ananimlib.DoubleArrow
   :members:

Grid
^^^^

.. autoclass:: ananimlib.Grid
   :members:

Line
^^^^

.. autoclass:: ananimlib.Line
   :members:

Rectangle
^^^^^^^^^

.. autoclass:: ananimlib.Rectangle
   :members:

Text AnObjects
---------------

Text
^^^^

.. autoclass:: ananimlib.Text
   :members:

TexMath
^^^^^^^

.. autoclass:: ananimlib.TexMath
   :members:

Number
^^^^^^

.. autoclass:: ananimlib.Number
   :members:

TextBox
^^^^^^^

.. autoclass:: ananimlib.TextBox
   :members:

Plotting AnObjects
------------------

CoordGrid
^^^^^^^^^

.. autoclass:: ananimlib.CoordGrid
   :members:

CoordAxis
^^^^^^^^^

.. autoclass:: ananimlib.CoordAxis
   :members:

PlotPoints
^^^^^^^^^^

.. autoclass:: ananimlib.PlotPoints
   :members:

PlotMark
^^^^^^^^

.. autoclass:: ananimlib.PlotMark
   :members:

Base AnObject Classes
---------------------

AnObject
^^^^^^^^

.. autoclass:: ananimlib.anobject.AnObject
   :members:

BezierAnObject
^^^^^^^^^^^^^^

.. autoclass:: ananimlib.BezierAnObject
   :members: 
   
ImageAnObject
^^^^^^^^^^^^^

.. autoclass:: ananimlib.ImageAnObject
   :members: 

CompositeAnObject
^^^^^^^^^^^^^^^^^

.. autoclass:: ananimlib.CompositeAnObject
   :members:

SVGAnObject
^^^^^^^^^^^

.. autoclass:: ananimlib.SVGAnObject
   :members:


Basic Instructions
------------------

AddAnObject
^^^^^^^^^^^

.. autoclass:: ananimlib.AddAnObject
   :members:

RemoveAnObject
^^^^^^^^^^^^^^

.. autoclass:: ananimlib.RemoveAnObject
   :members:

Wait
^^^^

.. autoclass:: ananimlib.Wait
   :members:

MoveTo
^^^^^^

.. autoclass:: ananimlib.MoveTo
   :members:

Move
^^^^

.. autoclass:: ananimlib.Move
   :members:

Rotate
^^^^^^

.. autoclass:: ananimlib.Rotate
   :members:

Scale
^^^^^

.. autoclass:: ananimlib.Scale
   :members:

AboutCenter
^^^^^^^^^^^

.. autoclass:: ananimlib.AboutCenter
   :members:

AboutLeft
^^^^^^^^^

.. autoclass:: ananimlib.AboutLeft
   :members:

AboutRight
^^^^^^^^^^

.. autoclass:: ananimlib.AboutRight
   :members:

AboutUpper
^^^^^^^^^^

.. autoclass:: ananimlib.AboutUpper
   :members:

AboutLower
^^^^^^^^^^

.. autoclass:: ananimlib.AboutLower
   :members:

AdjustAboutPoint
^^^^^^^^^^^^^^^^

.. autoclass:: ananimlib.AdjustAboutPoint
   :members:

SetAboutPoint
^^^^^^^^^^^^^

.. autoclass:: ananimlib.SetAboutPoint
   :members:

Draw
^^^^

.. autoclass:: ananimlib.Draw
   :members:

MoveCamera
^^^^^^^^^^

.. autoclass:: ananimlib.MoveCamera
   :members:

ZoomCamera
^^^^^^^^^^

.. autoclass:: ananimlib.ZoomCamera
   :members:

Emphasize
^^^^^^^^^

.. autoclass:: ananimlib.Emphasize
   :members:

FollowPath
^^^^^^^^^^

.. autoclass:: ananimlib.FollowPath
   :members:

AlignWithPath
^^^^^^^^^^^^^

.. autoclass:: ananimlib.AlignWithPath
   :members:

Swap
^^^^

.. autoclass:: ananimlib.Swap
   :members:

GrowArrow
^^^^^^^^^

.. autoclass:: ananimlib.GrowArrow
   :members:

DrawText
^^^^^^^^

.. autoclass:: ananimlib.DrawText
   :members:

Core Instructions
-----------------

RunSequential
^^^^^^^^^^^^^

.. autoclass:: ananimlib.RunSequential
   :members:

RunParallel
^^^^^^^^^^^

.. autoclass:: ananimlib.RunParallel
   :members:

SetAttribute
^^^^^^^^^^^^

.. autoclass:: ananimlib.SetAttribute
   :members:

SlideAttribute
^^^^^^^^^^^^^^

.. autoclass:: ananimlib.SlideAttribute
   :members:

Base Instruction Classes
------------------------

Instruction
^^^^^^^^^^^

.. autoclass:: ananimlib.Instruction
   :members:

InstructionTree
^^^^^^^^^^^^^^^

.. autoclass:: ananimlib.InstructionTree
   :members:

Renderers
---------

Render
^^^^^^

.. autoclass:: ananimlib.Render
   :members:

CairoRender
^^^^^^^^^^^

.. autoclass:: ananimlib.CairoRender
   :members:

ImageRender
^^^^^^^^^^^

.. autoclass:: ananimlib.ImageRender
   :members:

CompositeRender
^^^^^^^^^^^^^^^

.. autoclass:: ananimlib.CompositeRender
   :members:

BezierRender
^^^^^^^^^^^^

.. autoclass:: ananimlib.BezierRender
   :members:

Pen
^^^

.. autoclass:: ananimlib.Pen
   :members:

Bezier Utilities
----------------

BezierCurve
^^^^^^^^^^^

.. autoclass:: ananimlib.BezierCurve
   :members:

PolyBezier
^^^^^^^^^^

.. autoclass:: ananimlib.PolyBezier
   :members:

SVGPolyBezier
^^^^^^^^^^^^^

.. autoclass:: ananimlib.SVGPolyBezier
   :members:

