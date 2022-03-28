# -*- coding: utf-8 -*-
"""
Created on Sun Aug  8 17:10:18 2021
Generate all figures for the Quickstart chapter

@author: G. Ruch

"""
from collections import namedtuple
from os import path

import quickstart_ex1 
import quickstart_ex2 
import quickstart_ex3  
import quickstart_ex4
import quickstart_ex5
import quickstart_ex5_1
import quickstart_ex6
import quickstart_ex6_1
import quickstart_ex7


import ananimlib as al

al._defaults['frame_rate'] = 50
al._defaults['DPI'] = 50

base_path = '../'

figure = namedtuple("figure", ['file_name','func'] )
    
def main():
    
    
    figures = [
        figure("quickstart_ex1.gif",quickstart_ex1.run),
        figure("quickstart_ex2.gif",quickstart_ex2.run),
        figure("quickstart_ex3.gif",quickstart_ex3.run),
        figure("quickstart_ex4.gif",quickstart_ex4.run),
        figure("quickstart_ex5.gif",quickstart_ex5.run),
        figure("quickstart_ex5_1.gif",quickstart_ex5_1.run),
        figure("quickstart_ex6.gif",quickstart_ex6.run),
        figure("quickstart_ex6_1.gif",quickstart_ex6_1.run),
        figure("quickstart_ex7.gif",quickstart_ex7.run),
    ]

    for fig in figures:
        print(f"creating {fig.file_name}")
        m = fig.func()
        m.backend.save_gif(path.join(base_path,fig.file_name))
    
if __name__=="__main__":
    main()
    
