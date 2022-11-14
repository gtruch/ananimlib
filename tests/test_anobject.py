# -*- coding: utf-8 -*-
"""
Created on Tue Jun  1 13:58:56 2021

@author: Fred
"""

import pytest


@pytest.fixture
def container():
    import ananimlib as al
    return al.CompositeAnObject()

@pytest.fixture
def anobject():
    import ananimlib as al 
    return al.BezierAnObject()

@pytest.fixture
def container_with_keys(container,anobject):
    container.add_anobject(anobject,"thing")
    return anobject,container

@pytest.fixture
def container_no_keys(container,anobject):
    container.add_anobject(anobject)
    return anobject,container

def test_AnObjectContainer(container_with_keys):
    
    thing, cont  = container_with_keys
    
    # Retrieve the mobject and make sure the same object comes out
    assert(cont["thing"] is thing)    
    
def test_AnObjectContainer_index_by_anobject(container_no_keys):

    thing, cont = container_no_keys
    
    # Retrieve it and make sure the same object comes out
    assert(cont[thing] is thing)
    
def test_AnObjectContainer_with_keys_index_by_anobject(container_with_keys):

    thing, cont  = container_with_keys
    
    # Retrieve it and make sure the same object comes out
    assert(cont[thing] is thing)
    

def test_CompositeAnObject_index_by_key():
    import ananimlib as al
        
    # Create the composite
    comp = al.CompositeAnObject()
    
    # Create an anobject to add
    thing = al.BezierAnObject()

    # Add it to the composite
    comp.add_anobject(thing,"thing")
    
    # Retrieve it and make sure the same object comes out
    assert(comp["thing"] is thing)    
    
def test_CompositeAnObject_index_by_anobject_no_key():
    import ananimlib as al
        
    # Create the composite
    comp = al.CompositeAnObject()
    
    # Create a mobject to add
    thing = al.BezierAnObject()
    
    # Add it to the composite
    comp.add_anobject(thing)
    
    # Retrieve it and make sure the same object comes out
    assert(comp[thing] is thing)    
    
def test_CompositeAnObject_index_by_anobject_with_key():
    import ananimlib as al
        
    # Create the composite
    comp = al.CompositeAnObject()
    
    # Create a mobject to add
    thing = al.BezierAnObject()
    
    # Add it to the composite
    comp.add_anobject(thing,"thing")
    
    # Retrieve it and make sure the same object comes out
    assert(comp[thing] is thing)    
    
def test_CompositeAnObject_index_by_iterable():
    import ananimlib as al
        
    # Create two composites
    comp1 = al.CompositeAnObject()
    comp2 = al.CompositeAnObject()
    
    # Create a mobject to add
    thing = al.BezierAnObject()
    
    # Add it to the composite
    comp1.add_anobject(thing,"thing")
    comp2.add_anobject(comp1,"comp1")
    
    # Retrieve it and make sure the same object comes out
    assert(comp2["comp1","thing"] is thing)    

def test_CompositeAnObject_index_by_iterable_of_anobjects():
    import ananimlib as al
        
    # Create two composites
    comp1 = al.CompositeAnObject()
    comp2 = al.CompositeAnObject()
    
    # Create anobject to add
    thing = al.BezierAnObject()
    
    # Add it to the composite
    comp1.add_anobject(thing)
    comp2.add_anobject(comp1)
    
    # Retrieve it and make sure the same object comes out
    assert(comp2[comp1,thing] is thing)    
    