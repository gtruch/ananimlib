# -*- coding: utf-8 -*-
"""
Created on Sun Aug  8 17:09:43 2021

@author: Fred
"""

import ananimlib as al

def more_complex_ex1():
    rect = al.Rectangle([1,1])

    al.Animate(
        al.AddAnObject(rect),
        al.MoveTo(rect, [-3,0]),
        al.Move(rect, [6,0], duration=1.0),
        al.Wait(1.0),
    )

    al.play_movie()

if __name__ == "__main__":
    more_complex_ex1()