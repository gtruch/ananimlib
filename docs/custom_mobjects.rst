More Complex Animations
=======================

Animations created with AnAnimLib consist of creating *AnObjects* that represent
graphical objects and using *Instructions* to modify their attributes. For
example, the *Move* and *MoveTo* instructions modify the *position* attribute of
the *AnObject* on which they operate. Complex animations can be created by
creating classes that inherit from one of the base *AnObject* classes, defining
custom attributes that control their appearance, and maniuplating those
attributes using *Instructions*.

SetAttribute and SlideAttribute
-------------------------------

Many instructions, inherit from one of two core instructions; *SetAttribute*,
which sets an attribute to a particular value,  and *SlideAttribute*, which
"slides" an attribute through a range of values. The snippets below demonstrate
two ways to perform a move; using *Move* and *MoveTo* or using *SetAttribute*
and *SlideAttribute*.

.. code-block:: 
    :linenos:

    import ananimlib as al        
    
    rect = al.Rectangle([1,1])
    
    al.Animate(
        al.AddAnObject(rect),
        al.MoveTo(rect, [-3,0]),
        al.Move(rect, [6,0], duration=1.0),
        al.Wait(1.0)
    )
    
    al.play_movie()    


.. code-block::
    :linenos:

    m = ml.iManim()

    rect = ml.Rectangle([1,1])

    m.run(
        ml.AddMobject(rect),
        ml.SetAttribute(rect, "position", [-3,0]),
        ml.AdjustAttribute(rect, "position", [3,0], duration=1.0),
        ml.Wait(1.0),
    )

    m.play_movie()

The output from both snippets is the same:

.. figure:: quickstart_example2.gif
    :class: with-border
    :width: 95%
    :align: center
    
    stuff

Both *SetAttribute* and *SlideAttribute* take as parameters the *AnObject*, the name
of the attribute to manipulate, a value to assign that attribute, and an
optional duration.  Here is how the Move instruction is implemented:

.. code-block::
    :linenos:

    class Move(al.SlideAttribute):
        """Move an AnObject relative its current position

        Parameters
        ----------
        key: string or AnObject 
            The AnObject to move

        displacement: Vector
            The new coordinates of the mobject in Scene Units

        duration: optional float
            The amount of time over which to move the mobject.
            default = 0.0, instantaneous

        transfer_func: optional callable
            The transfer function maps the ratio of time elapsed over total time to the
            fraction of the total move distance.  
            ratio = transfer_func(alpha)
            default = smooth
        """

        def __init__(self, key, displacement, duration=0.0,
                     transfer_func=al.smooth):
            super().__init__(key         = key,
                            attribute  = 'position',
                            end_value  = displacement,
                            duration   = duration,
                            transfer_func = transfer_func)

Since *SetAttribute* and *SlideAttribute* operate on an arbitrary attribute, our
custom instruction need only pass the name of that attribute and any other
required parameters to the *__init__* method of the parent class.  

