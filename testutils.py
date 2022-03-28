# -*- coding: utf-8 -*-
"""
Utilities for testing and construction

Created on Mon Oct 21 12:02:32 2019

@author: Gtruch
"""

import manimlib2.Camera
import pygame as pg
import numpy as np



def buildTestCam(DPI=None, frame_height=8.0, frame_width=8.0,
                 pixel_width=1280,pixel_height=720,
                 frame_rate=60,
                 camera_x_center=0.0,camera_y_center=0.0,
                 camera_rotation=0.0):
    """Build a test camera to examine renderings of still scenes"""
    
    if DPI is not None:
        pixel_width  = DPI*frame_width
        pixel_height = DPI*frame_height
    
    return manimlib2.Camera.Camera(pixel_width, pixel_height,
                                   frame_height,frame_rate,
                                   frame_width,
                                   camera_x_center,camera_y_center,
                                   camera_rotation)

# def buildTestCam(pixel_width=1280,pixel_height=720,
#                  frame_height=8.0,frame_rate=60,
#                  frame_width=0.0,
#                  camera_x_center=0.0,camera_y_center=0.0,
#                  camera_rotation=0.0):
#     """Build a test camera to examine renderings of still scenes"""
    
#     return manimlib2.Camera.Camera(pixel_width, pixel_height,
#                                    frame_height,frame_rate,
#                                    frame_width,
#                                    camera_x_center,camera_y_center,
#                                    camera_rotation)
          
                         
def static_test(DPI=75,width=25,height=25):
    """A dynamic decorator that provides a camera instance"""
    camera = None
    def deco(func):
        def inner():
            
            nonlocal camera
        
            camera = buildTestCam(pixel_width=DPI*width,
                                     pixel_height=DPI*height,
                                     camera_x_center=0.0,
                                     camera_y_center=0.0,
                                     frame_width=width,
                                     frame_height=height) 
        
            func(camera)
            
            pgShowFrame(camera)   
        return inner
    return deco

def pgShowFrame(camera):
    """Show the current camera frame in a PyGame window."""
    
    pg.init()

    # initialize the display
    screen = pg.display.set_mode(camera.pixelsPerFrame)
    done = False

    #display the frame        
    f = np.transpose(camera.frame[:,:,:3],[1,0,2])        
    pg.surfarray.blit_array(screen,f)
    pg.display.flip()
    
    while not done:   # Some event triggers done
 
        # Handle Events.
        for event in pg.event.get():
            
            if event.type == pg.QUIT:
                done = True
                
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    done = True
    pg.quit()
