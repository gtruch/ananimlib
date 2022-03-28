



def test_composite_anobject_data_struct():
    import ananimlib as al
        
    # Create resources
    c0 = al.CompositeAnObject()   
    c1 = al.CompositeAnObject()
    c2 = al.CompositeAnObject()
    o0 = al.Rectangle([1,1])
    o1 = al.Rectangle([1,1])
    o2 = al.Rectangle([1,1])
    o3 = al.Rectangle([1,1])
    o4 = al.Rectangle([1,1])
    
    # Add a rectangle to the composite with a key
    c0.add(o0,"Obj0")
    
    # Add a rectangle to the composite without a key
    c0.add(o1)
    
    ###########################
    # Test stage 1 - One level
    ###########################

    # Retrieve the rectangle to ensure we get the same one out.
    assert(c0.get(o0) is o0)        # fetch by AnObject ref
    assert(c0.get("Obj0") is o0)    # fetch by key
    assert(c0.get(o1) is o1)

    ############################
    # Test stage 2 - Two levels
    ############################

    # Add another composite to the composite
    c0.add(c1,"Composite1")
    
    # Add an AnObject to Composite1 through Composite1
    c1.add(o2,"Obj2")    
    
    # Retrieve through Composite 0
    assert(c0.get(['Composite1','Obj2']) is o2)

    
    # Add an AnObject to Composite1 through Composite0
    c0.add(o3,"Obj3",path=['Composite1'])    
    
    # Retrieve through Composite 0
    assert(c0.get(['Composite1','Obj3']) is o3)
    
    
    ##############################
    # Test stage 3 - Three levels
    ##############################
    
    # Add a composite to Composite1
    c1.add(c2,'Composite2')
    
    # Add anobject to Composite2 through Composite0
    c0.add(o4,'obj4',path=['Composite1','Composite2'])
    
    # Retrieve through Composite 0
    assert(c0.get(['Composite1','Composite2','obj4']) is o4)
    
    
if __name__=="__main__":
    test_composite_anobject_data_struct()