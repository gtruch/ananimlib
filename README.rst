
============================================================
Welcome to *AnAnimLib*
============================================================

.. image:: docs/images/Logo.gif
  :width: 100%

|

AnAnimlib was inspired by `ManimLib <https://github.com/3b1b/manim>`_ by Grant
Sanderson of `3Blue1Brown <https://www.youtube.com/c/3blue1brown>`_.  The aim of AnAnimlib is to facilitate the creation
of mathematically preceise animations through an intuitive and extensible API.

As a simple example, the following code spins a square it as it moves across the canvas.

.. code-block:: python

    import ananimlib as al

     rect = al.Rectangle([1,1])

     al.Animate(
         al.AddAnObject(rect),
         al.MoveTo(rect,[-3.0,0.0]),
         al.RunParallel(
             al.Move(rect, [6,0], duration=1.0),
             al.Rotate(rect, 2*3.1415, duration=1.0),
         ),
         al.Wait(1.0)
    )

    al.play_movie()


.. image:: docs/images/quickstart_ex3.gif
    :width: 95%
    :align: center
 

Installation instructions:

.. code-block::

    > pip install ananimlib
    
Documentation available at `Read The Docs <https://ananimlib.readthedocs.io/en/latest/index.html>`_
