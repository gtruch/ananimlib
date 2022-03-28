# -*- coding: utf-8 -*-
"""
Created on Tue Sep 21 10:10:57 2021

@author: Fred
"""

from livereload import Server, shell

def main():
    server = Server()
    server.watch('*.rst', shell('make html'))
    server.serve(root='_build/html')


if __name__=="__main__":
    main()

