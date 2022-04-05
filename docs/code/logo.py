# -*- coding: utf-8 -*-
"""
Created on Sat Apr  2 21:20:12 2022

@author: Fred
"""

import numpy      as np
import ananimlib  as al
import simulation as sim

def main():
    
    
    # Tune the camera parameters
    al.engine.config_camera(width = 11, 
                            ar    = 11/7, 
                            frame_rate = 50, 
                            DPI = 55)    
    
    al.Animate(

        # Run the simulation and draw the title simultaneously
        al.RunParallel(
            
            # Start the simulation and let it run
            slide_simulation(key='sim'),
            
            # Let the sim run for awhile then draw the title
            al.RunSequential(
                al.Wait(4),
                
                # Move the simulation down and shrink it while drawing the title
                al.RunParallel(
                    al.Scale('sim', 0.9,duration=1.0),
                    al.Move('sim', [0,-0.5],duration=1.0),
                    draw_title()
                ),
                al.Wait(1.5),
                al.RunParallel(*[
                    al.Emphasize(key, scale_mult=1.2, duration=0.75)
                        for key in ['Another','Animation','Library']]
                )
            )
        ),
        al.Wait(10.0)
    )

    al.play_movie()                         # Play the movie in a window
#    al.engine.backend.save_mp4("Logo.mp4")  # Save the movie as an mp4
    al.engine.backend.save_gif("Logo.gif")


def draw_title():
        
    text_list = [    "Another", "Animation",  "Library"]
    size_list = [            2,           4,         3]
    pos_list  = [ [-2.23, 2.8],     [0,2.8], [2.3,2.78]]
    
    tt1 = []
    tt2 = []
    instructions = []
    for tt,sz, pp in zip(text_list, size_list, pos_list):
        text1 = al.Text(tt)
        text1.about_center()
        text1.scale = 1.5
        text2 = text1.get_anobject(slice(0,sz))
        text2.about_center()
        text2.set_pen(al.Pen(fill_color="#cda448",                                      
                                 fill_opacity=1.0,
                                 stroke_width = 2.0))

        instructions.extend((
            al.AddAnObject(text1),
            al.DrawText(text1, duration=1.0),
            al.Wait(1.0),
            al.AddAnObject(text2,key=tt),
            al.SlideAttribute(text1, 'opacity', 0, duration=1.0),
            al.MoveTo(text2, pp,duration=1.0)
                        
        ))
        
    return al.RunSequential(*instructions)

    
def slide_simulation(key=None):

    if key is None: 
        key = 'grid'

    dots = [[0,2.2],[3,1],[4.2,1.945], [6,0],[7,3]]

    path = al.PolyBezier()
    path.connect_smooth(dots)
    path_ob = al.BezierAnObject(path=path,pen=al.Pen(stroke_width=2.0))
                
    g = 4.0
    
    box = SlidyBox(0.1,0.0,path,g=g)

    def pos_func(time,timing): 
        box.model.advance(timing.time_used)            
        return box.model.u

    grid =  al.CoordGrid([10,6], [10,6], [1,1], [.2,.2], offset=[-2.5,-2])
    grid.add_anobject(path_ob)
    grid.add_anobject(box,'box')

    return al.RunSequential(
        al.AddAnObject(grid,key),
        al.SetAttribute([grid,box], 'u', pos_func, duration=15.4),            
    )

class SlidyBox(al.CompositeAnObject):
    """A box that follows a path under control of some physics

    Attributes
    ----------    
    u : float
        The parameter describing the box's position along the path
        
    path : PolyBezier
        The path along which slidybox slides
    """
    
    def __init__(self, u0, v0, path, g=9.81):
        """Get it set up.
        
        Parameters
        ----------
        path : PolyBezier
            The path along which the slidybox slides
        """
        super().__init__()

        self.model = ConstrainedBeadModel(u0, v0, path, g=g)
        self.path = path    
        self.g=g

        label_scale = 0.5
        arrow_head_size = 0.5
        arrow_stroke_width = 2.0

        box =  al.Rectangle([.3,.3],pen=al.Pen(fill_color="#cda448",                                      
                                               fill_opacity=1.0,) )
        box.about_lower()
        box.position = [0.0,0.0]
        self.add_anobject(box,'box')

        # Build the ds arrow and label.  
        ds =  al.Arrow([0.0,0.0], [0.5,0],head_size=arrow_head_size,
                       pen = al.Pen(stroke_width = arrow_stroke_width))
        ds.about_point = [-0.2,-0.15]
        ds.position = [0.0,0.0]

        dslabel = al.TexMath("d \\vec s")
        dslabel.scale = label_scale
        ds.add_anobject(dslabel,'label')
        dslabel.position = [.7,0]
#        self.add_mobject(ds,'ds')

        # Build the Fn arrow and label
        fn =  al.Arrow([0.0,0.0], [0.5,0],head_size=arrow_head_size,
                       pen = al.Pen(stroke_width = arrow_stroke_width))
        fn.about_point = [-0.32,-0.0]
        fn.position=[0.0,0.0]
        
        fnlabel = al.TexMath("\\vec{F}_n")
        fnlabel.scale = label_scale
        fn.add_anobject(fnlabel,'label')
        fnlabel.position = [1.0,0]
        fnlabel.rotation_angle = -np.pi/2
        self.add_anobject(fn,"fn")

        # Build the mg arrow and label
        mg = al.CompositeAnObject([ al.Arrow([0.0,-0.0],[0.0,-.5],head_size=arrow_head_size,
                       pen = al.Pen(stroke_width = arrow_stroke_width))])
        glabel = al.TexMath("m \\vec g")
        glabel.scale=label_scale
        mg.add_anobject(glabel)
        glabel.position = [0.0,-0.7]
        self.add_anobject(mg,'mg')
        
        
        self.u = self.model.u
         
       
    @property
    def u(self):
        return self._u
    
    @u.setter
    def u(self,val):

        self._u = val
        self.position = self.path.B(self.u)
        
        slope = self.path.Bprime(self.u)
        theta =  al.Vector(slope).theta

        self.get_anobject("box").rotation_angle = theta
#        self["ds"].rotation_angle  = theta

        self.get_anobject("fn").rotation_angle = theta+np.pi/2
        fnmag = self.model.Fn*0.5/self.g

        self.get_anobject("fn").magnitude = fnmag
        self.get_anobject(["fn","label"]).position = [fnmag+0.15,0]
        return
                    
class ConstrainedBeadModel(sim.PhysModel):
    """A model of a particle constrained to a parameterized path.

    Attributes
    ----------
    u : float
        The Bezier parameter the describing the bead's 
        position along the path
        
    ud : float
        The time derivative of the Bezier parameter.  (u-dot)
        
    position : read only Vector
        The position of the particle

    velocity : read only Vector
        The velocity of the particle
                        
    """
    
    def __init__(self,u0,v0,path,g=9.81):
        """Build the model 
        
        Parameters
        ----------
        u0 : float
            The initial value of the position parameter u
            
        v0 : float
            The magnitude of the initial velocity of the particle
        
        path : PolyBezier
            A polybezier curve describing the path of that the bead is 
            constrained to
        g : float, optional
            The acceleration due to gravity.
            default = 9.91 m/s/s
        """
        
        self.g=g
        
        # Calculate du/dt from u and v0
        ud = v0/np.sqrt(np.sum(path.Bprime(u0)**2))

        self.bead = Bead(u0,ud,path)
        
        super().__init__(physics=BeadPhys(sim.RK4(),g=g),
                         body=self.bead,
                         dt_max=0.01)
    @property
    def path(self):
        return self.bead.path
    
    @property        
    def u(self):
        return self.bead.u
    
    @property
    def ud(self):
        return self.bead.ud
    
    @property
    def position(self):
        return self.bead.position
    
    @property
    def velocity(self):
        return self.bead.velocity
        
    @property
    def Fn(self):
        """Calculate the normal (constraint) force"""
        rp  =  al.Vector(self.bead.path.Bprime(self.u))
        rpp =  al.Vector(self.bead.path.Bdprime(self.u))
        
        return self.g*rp[0]/rp.mag+self.ud**2*(rp[0]*rpp[1]-rpp[0]*rp[1])

class Bead():
    """Hold Bezier parameter and perform conversions.  
    
    Attributes
    ----------
    u : float
        The Bezier parameter.  
        0 <= u <= 1
    
    udot : float
        udot, the time derivative of u.  
        
    pos : read only Vector
        A vector representing the position of the particle.
        
    vel :  Vector
        A vector representing the velocity of the particle
    
    path : PolyBezier
        The curve to which the body is constrained
    """
    
    def __init__(self, u, ud, path):
        self.state = np.array([u,ud])
        self.path  = path
        

    @property        
    def u(self):
        return self.state[0] 
    
    @u.setter
    def u(self,val):
        self.state[0] = val

    @property
    def ud(self): 
        return self.state[1]
    
    @property        
    def position(self):
        return  al.Vector(self.path.B(self.u))
        
    @property 
    def velocity(self):

        # rdot = udot*rprime
        return self.ud* al.Vector(self.path.Bprime(self.u))



class BeadPhys(sim.Physics):
    """ Bezier Curve Physics

    Attributes
    ----------
    path : manimlib2.PolyBezier
        The Bezier Path
    """

    def __init__(self, solver,g=9.81):
        """Initialize.

        Parameters
        ----------
        solver : Solver
            An instance of a class derived from Solver to solve the differential
            equation
        """
        self.g=g
        super().__init__(solver)

    def advance(self, t, body, dt):
        """Advance the pendulum one time step

        Parameters
        ----------
        t: float
            The current time

        body : BezBody
            Bezier Body

        dt: float
            The time step
        """
        self.body = body
        t, body.state = self.solver.advance(t,body.state,dt)
        return t,body
    
        
    def diff_eq(self, t, f):
        """Pendulum differential equation

        Parameters
        ----------
        t : float
            The current time

        f : array of floats
            The Bezier Parameter
        """
        u = f[0]   # u
        ud = f[1]  # u dot (velocity)

        rp = self.body.path.Bprime(u)
        rdp = self.body.path.Bdprime(u)
#        ud = self.body._vmag_to_udot(vmag,u)
        ss = np.sum(rp**2)
    
        
        # u dot dot (acceleration)
        udd = ((-ud**2)*(np.sum(rp*rdp))-self.g*rp[1])/ss
        
    
        return np.array([ud,udd])

def draw_title2():
    
    title = al.CompositeAnObject()
    title_text = [al.Text(c) for c in "AnAnimLib"]
    
    radius = 3.0
    theta_start = 135
    theta_end = theta_start-90

    dtheta = (theta_end-theta_start)/len(title_text)*np.pi/180
    theta = theta_start*np.pi/180-np.pi/2
    for letter in title_text:
        letter.about_point = [0,-radius]
        letter.rotation_angle = theta
        letter.position = [0,0]
        theta += dtheta
        
        title.add_anobject(letter)
    
    return al.RunSequential(
                al.AddAnObject(title)
        )
            
def draw_title1():
    
    title = al.Text("AnAnimLib", pen=al.Pen(fill_color="#cda448",                                      
                                            fill_opacity=1.0,))
    title.scale  = 2.0
    title.position = [0,3]
    
    return al.RunSequential(
        al.AddAnObject(title),
        al.DrawText(title, duration=4.0)
    )

if __name__ == "__main__":
    main()