# -*- coding: utf-8 -*-
"""
Created on Tue Jun  1 13:58:56 2021

@author: Fred
"""

import pytest


@pytest.fixture
def container():
    import manimlib2 as ml
    return ml.MobjectContainer()

@pytest.fixture
def mobject():
    import manimlib2 as ml
    return ml.VMobject()

@pytest.fixture
def container_with_keys(container,mobject):
    container.add_mobject(mobject,"thing")
    return mobject,container

@pytest.fixture
def container_no_keys(container,mobject):
    container.add_mobject(mobject)
    return mobject,container

def test_MobjectContainer(container_with_keys):
    
    thing, cont  = container_with_keys
    
    # Retrieve the mobject and make sure the same object comes out
    assert(cont["thing"] is thing)    
    
def test_MobjectContainer_index_by_mobject(container_no_keys):

    thing, cont = container_no_keys
    
    # Retrieve it and make sure the same object comes out
    assert(cont[thing] is thing)
    
def test_MobjectContainer_index_by_mobject(container_with_keys):

    thing, cont  = container_with_keys
    
    # Retrieve it and make sure the same object comes out
    assert(cont[thing] is thing)
    



def test_CompositeMobject_index_by_key():
    import manimlib2 as ml
        
    # Create the composite
    comp = ml.CompositeMobject()
    
    # Create a mobject to add
    thing = ml.VMobject()
    
    # Add it to the composite
    comp.add_mobject(thing,"thing")
    
    # Retrieve it and make sure the same object comes out
    assert(comp["thing"] is thing)    
    
def test_CompositeMobject_index_by_mobject_no_key():
    import manimlib2 as ml
        
    # Create the composite
    comp = ml.CompositeMobject()
    
    # Create a mobject to add
    thing = ml.VMobject()
    
    # Add it to the composite
    comp.add_mobject(thing)
    
    # Retrieve it and make sure the same object comes out
    assert(comp[thing] is thing)    
    
def test_CompositeMobject_index_by_mobject_with_key():
    import manimlib2 as ml
        
    # Create the composite
    comp = ml.CompositeMobject()
    
    # Create a mobject to add
    thing = ml.VMobject()
    
    # Add it to the composite
    comp.add_mobject(thing,"thing")
    
    # Retrieve it and make sure the same object comes out
    assert(comp[thing] is thing)    
    
def test_CompositeMobject_index_by_iterable():
    import manimlib2 as ml
        
    # Create two composites
    comp1 = ml.CompositeMobject()
    comp2 = ml.CompositeMobject()
    
    # Create a mobject to add
    thing = ml.VMobject()
    
    # Add it to the composite
    comp1.add_mobject(thing,"thing")
    comp2.add_mobject(comp1,"comp1")
    
    # Retrieve it and make sure the same object comes out
    assert(comp2["comp1","thing"] is thing)    

def test_CompositeMobject_index_by_iterable_of_mobjects():
    import manimlib2 as ml
        
    # Create two composites
    comp1 = ml.CompositeMobject()
    comp2 = ml.CompositeMobject()
    
    # Create a mobject to add
    thing = ml.VMobject()
    
    # Add it to the composite
    comp1.add_mobject(thing)
    comp2.add_mobject(comp1)
    
    # Retrieve it and make sure the same object comes out
    assert(comp2[comp1,thing] is thing)    
    