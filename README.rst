ManimLib2
=========

ManimLib2 is inspired by `ManimLib <https://github.com/3b1b/manim>`_ by Grant Sanderson of 3b1b.  ManimLib2 facilitates the creation of mathematically preceise animations through an easy to use API.

For example, the following code draws a rectangle and spins it as it flies across the screen::

    # Create an instance of the animation engine
    m = Manim.iManim("")

    # Create an object to animate
    rect = cmob.Rectangle([1,2])
    rect.position = [-4,0]

    # Issue instructions to the renderer
    m.run(
        i.AddMobject('rect', rect),
        m.runParallel(
            i.MoveTo('rect',[4,0],duration=1.0),
            i.Rotate('rect', 2*np.pi,duration=1.0)
        )
    )

    # Play the rendered animation
    m.play_movie()

Features
--------

- Easy to use animation engine.
- Easily extensible API making it simple to create additional animation objects and animation instructions.

Installation
------------

Download the code and add the manimlib2 directory do your python path.  


Set Up Development Environment 
------------------------------

#. Clone the repository to your local drive making note of the path.  

#. Open an Anaconda Prompt and navigate to the manimlib2 directory.  

#. Create a conda environment with all of the requisite packages by issuing the following command:

        conda env create -f environment.yml
        
#. You should see a new `Spyder (manim2)` icon on the start menu that automatically opens spyder in the new environment.  

#. Add the manimlib2 directory to your python path.  In Spyder, use the Python Path manager on the Tools menu.  

#. Open `basics.py` in the Tutorials directory.  If it runs, you win!  



