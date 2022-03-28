# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 15:39:32 2021

@author: Fred
"""

def test_run_sequential():
    import ananimlib as al
    
    i1 = al.Wait(1.0)
    i2 = al.Wait(1.0)
    i3 = al.Wait(1.0)
    
    rs = al.RunSequential(i1,i2,i3)
    
    # We should have only the first Wait instruction, i1, queued up.
    assert(len(rs.current_instructions) == 1)
    assert(rs.current_instructions[0] is i1)
    
    # i1 should have only i2 in its next_instructions list
    assert(len(i1.next_instructions)==1)
    assert(i1.next_instructions[0] is i2)
    
    # i2 should have only i3 
    assert(len(i2.next_instructions)==1)
    assert(i2.next_instructions[0] is i3)

     #i3 should have an empty next_instructions
    assert(len(i3.next_instructions)==0)
    
        
def test_run_parallel():
    import ananimlib as al
    
    i1 = al.Wait(1.0)
    i2 = al.Wait(1.0)
    
    rp = al.RunParallel(i1,i2)
    
    # i1 and i2 should both be in the current_instructions list.
    assert(len(rp.current_instructions)==2)
    assert(rp.current_instructions[0] is i1)
    assert(rp.current_instructions[1] is i2)
    
    # next_instructions should be empty for everyone
    assert(len(rp.next_instructions)==0)
    assert(len(i1.next_instructions)==0)
    assert(len(i2.next_instructions)==0)
    

def test_swap():
    import ananimlib as al
    
    # make two an anobjects whose positions will be swapped
    obj1 = al.Rectangle([1,1])
    obj2 = al.Rectangle([1,1])
    
    # Set their positions
    obj1.position = [2,1]
    obj2.position = [1,2]
    
    # Add them to a scene
    scene = al.Scene(None)
    scene.add_anobject(obj1)
    scene.add_anobject(obj2)
    
    # Create an instance of the swap instruction
    swap = al.Swap(obj1,obj2,duration=1.0)
    
    # Send the start signal
    swap.start(scene)
            
    # Update the tree until all is finished
    while(not swap.finished):
        swap.update(scene, 0.1)
        
    assert((obj1.position == al.Vector([1,2])).all())
    assert((obj2.position == al.Vector([2,1])).all())
    
def test_composite_swap():
    """Use swap to swap anobjects inside of a composite anobject"""
    import ananimlib as al

    # make two an anobjects whose positions will be swapped
    obj1 = al.Rectangle([1,1])
    obj2 = al.Rectangle([1,1])
    
    # Set their positions
    obj1.position = [2,1]
    obj2.position = [1,2]
    
    # Put them in a composite anobject
    composite = al.CompositeAnObject([obj1,obj2])
    
    # Add the composite to a scene
    scene = al.Scene(None)
    scene.add_anobject(composite)
    
    # Create an instance of the swap instruction
    swap = al.Swap([composite,0],[composite,1],duration=1.0)
    
    # Send the start signal
    swap.start(scene)
            
    # Update the tree until all is finished
    while(not swap.finished):
        swap.update(scene, 0.1)
        
    assert((obj1.position == al.Vector([1,2])).all())
    assert((obj2.position == al.Vector([2,1])).all())
    
    
if __name__=="__main__":
    test_swap()
    test_composite_swap()
