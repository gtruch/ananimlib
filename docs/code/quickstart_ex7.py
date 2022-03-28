# -*- coding: utf-8 -*-
"""
Created on Tue Aug 17 11:15:17 2021

@author: Fred
"""
# START
import ananimlib as al
    
composite = al.CompositeAnObject()
composite.add_anobject(al.Rectangle([1,1]),   'rect')
composite.add_anobject(al.Arrow([0,0],[2,0]), 'arrow')

al.Animate(
      al.AddAnObject(composite),
      al.MoveTo(composite,[3,0], duration=1.0),
      al.Wait(0.5),
      
      al.MoveTo([composite,'arrow'], [0.5,0],duration=1.0),
      al.Wait(0.5),
      
      al.SetAboutPoint([composite,'arrow'], [-0.5,0.0]),
      al.Rotate([composite,'arrow'], 3.1415,duration=1.0),
      al.Wait(0.5),
      
      al.MoveTo(composite,[0,0],duration=1.0),
      al.Wait(0.5),
)
    
al.play_movie()
# END 
