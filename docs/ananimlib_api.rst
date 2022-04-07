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

Base Animation Objects (AnObjects)
----------------------------------

AnObject
^^^^^^^^

.. autoclass:: ananimlib.anobject.AnObject
   :members:

BezierAnObject
^^^^^^^^^^^^^^

.. autoclass:: ananimlib.anobject.BezierAnObject
   :members: 
   
ImageAnObject
^^^^^^^^^^^^^

.. autoclass:: ananimlib.anobject.ImageAnObject
   :members: 

CompositeAnObject
^^^^^^^^^^^^^^^^^

.. autoclass:: ananimlib.anobject.CompositeAnObject
   :members:

Derived Animation Objects
-------------------------

Line
^^^^

.. autoclass:: ananimlib.Line
   :members:

Circle
^^^^^^

.. autoclass:: ananimlib.Circle
   :members:

Arc
^^^

.. autoclass:: ananimlib.Arc
   :members:

Dot
^^^

.. autoclass:: ananimlib.Dot
   :members:

Arrow
^^^^^

.. autoclass:: ananimlib.Arrow
   :members:

DoubleArrow
^^^^^^^^^^^

.. autoclass:: ananimlib.DoubleArrow
   :members:

ArrowHead
^^^^^^^^^

.. autoclass:: ananimlib.ArrowHead
   :members:

EngineerPaper
^^^^^^^^^^^^^

.. autoclass:: ananimlib.EngineerPaper
   :members:

Rectangle
^^^^^^^^^

.. autoclass:: ananimlib.Rectangle
   :members:

Grid
^^^^

.. autoclass:: ananimlib.Grid
   :members:

CrossHair
^^^^^^^^^

.. autoclass:: ananimlib.CrossHair
   :members:



