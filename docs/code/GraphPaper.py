# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 08:59:56 2021

@author: Fred
"""

import manimlib2 as ml

m = ml.iManim()

m.config_camera(width = 16, 
                ar    = 16/12, 
                frame_rate = 30, 
                DPI = 120)

back = ml.Rectangle([16,12],pen=ml.Pen(fill_opacity=1.0))
graph = ml.CoordGrid([10,10], [10,10], [1,1], minor_spacing=[.2,.2],
                     origin = [-5,-5],
                     text_pen = ml.Pen(stroke_color = "#000",
                                       fill_color   = "#000",
                                       fill_opacity = 1.0),
                     major_pen = ml.Pen(stroke_color="#000",stroke_width=2.0),
                     minor_pen = ml.Pen(stroke_color   = "#000",
                                        stroke_width   = 1.0,
                                        stroke_opacity = 0.75),
                     axis_pen  = ml.Pen(stroke_color="#000",stroke_width=3.0))
graph.about_center()
graph.position = [0,0]

m.run(
    ml.AddMobject(back),
    ml.AddMobject(graph),
    ml.Wait(1.0)         
)

#m.play_movie()
m.backend.save_gif("graph.gif")
