# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 09:03:08 2020

@author: Fred
"""

import ananimlib as al

import copy  as cp
import numpy as np
import hashlib
import os
from xml.dom import minidom
import pdb
import subprocess as subp

# TODO: Some doc-strings would be nice hey?
# TODO: Add functionality to easily access each glyph for manipulation


class Text(al.SVGAnObject):
    """Uses Tex to render some text"""

    def __init__(self,text=None,pen=None,pre="",post=""):

        self.pre=pre
        self.post=post
        self._opacity=1.0
        self._fill_opacity=1.0
        self._stroke_opacity=0.0

        if pen is None:
            pen = al.Pen(fill_opacity=1.0)

        if text is None:
            super().__init__(rescale=0.08)
            return

        super().__init__(self._build_svg(pre+text+post),pen=pen,rescale=0.08)
        self.about_center()
        self.position = [0.0]
        
    

    @property
    def opacity(self):
        return self._opacity

    @opacity.setter
    def opacity(self, value):
        self._opacity=value
        for sym in self.keys:
            self.get_anobject(sym).fill_opacity = \
                    self._opacity*self._fill_opacity
            self.get_anobject(sym).stroke_opacity = \
                    self._opacity*self._stroke_opacity

    # def get_anobject(self, key):
        
    #     if isinstance(key,slice):
    #         new_composite = super().get_anobject(key)
    #         ret = Text()
    #         for ano in new_composite:
    #             ret.add_anobject(ano)
    #     else : 
    #         return super().get_anobject(key)


    def _build_svg(self,new_text):
        
        # TODO: Maybe... Cache some build data right here.  
        #       Numbers, in particular, get re-used often and 
        #       caching will speed up their creation
        self._text = new_text

        #  Make sure that the output directory works
        base_path = os.path.join(".",".tex")
        if not os.path.exists(base_path):
            os.makedirs(base_path)

        # Generate the body of the LaTex file
        tex_body = self._do_stuff(new_text)

        #Generate a file name
        tex_file_name = self._hash(tex_body) + ".tex"
        tex_file_name = os.path.join(base_path,tex_file_name)

        # Write the tex file
        with open(tex_file_name, "w", encoding="utf-8") as outfile:
            outfile.write(tex_body)

        # Run Latex
        dvi_file_name = self.tex_to_dvi(tex_file_name)

        # Run dvisvgm
        svg_file_name = self.dvi_to_svg(dvi_file_name)

        return svg_file_name



    def set_pen(self,pen):

        for sym in range(len(self)):
            self.get_anobject(sym).renderer.pen = cp.copy(pen)
            self._fill_opacity=pen.fill_opacity
            self._stroke_opacity=pen.stroke_opacity


    def _do_stuff(self,text):

        return (
            "\\documentclass[preview]{standalone}\n" +
            "\\usepackage[english]{babel}\n" +
            "\\usepackage{amsmath}\n" +
            "\\usepackage{amssymb}\n" +
            "\\usepackage{dsfont}\n" +
            "\\usepackage{setspace}\n" +
            "\\usepackage{tipa}\n" +
            "\\usepackage{relsize}\n" +
            "\\usepackage{textcomp}\n" +
            "\\usepackage{mathrsfs}\n" +
            "\\usepackage{calligra}\n" +
            "\\usepackage{wasysym}\n" +
            "\\usepackage{ragged2e}\n" +
            "\\usepackage{physics}\n" +
            "\\usepackage{xcolor}\n" +
            "\\usepackage{microtype}\n" +
#            "\\usepackage[UTF8]{ctex}\n" +
            "\\usepackage{harpoon}\n" +
            "\\newcommand*{\\vect}[1]{\\overrightharp{\\ensuremath{#1}}}\n" +
            "\\linespread{1}\n" +
            "\\begin{document}\n" +
            "%s\n"%(text) +
            "\\end{document}\n"
        )

    def _hash(self,text):

        hasher = hashlib.sha256()
        hasher.update(text.encode())

        # Truncating at 16 bytes for cleanliness
        return hasher.hexdigest()[:16]

    def tex_to_dvi(self,tex_file):
        base,file = os.path.split(tex_file)
        result = file.replace(".tex", ".dvi")
        if not os.path.exists(os.path.join(base,result)):
            commands = [
                "latex",
                "-interaction=batchmode",
                "-halt-on-error",
                "-output-directory=\"{}\"".format(base),
                "\"{}\"".format(file)
                # ">",
                # os.devnull
            ]
            cp = subp.run(commands, capture_output=True)
#            exit_code = os.system(" ".join(commands))
#            if exit_code != 0:
            if cp.returncode != 0:
#                pdb.set_trace()
                log_file = tex_file.replace(".tex", ".log")
                # print(os.getcwd())
                raise Exception(
                    f'{cp.stdout}' +
                    "Latex error converting to dvi. " +
                    "See log output above or the log file: %s" % log_file)
        return os.path.join(base,result)

    def dvi_to_svg(self, dvi_file, regen_if_exists=False):
        base,file=os.path.split(dvi_file)

        result = os.path.join(base,file.replace(".dvi", ".svg"))
        if not os.path.exists(result):
            commands = [
                "dvisvgm",
                "\"{}\"".format(dvi_file),
                "-n",
                "-v",
                "0",
                "-o",
                "\"{}\"".format(result),
                ">",
                os.devnull
            ]
            print(' '.join(commands))
            exit_code = os.system(" ".join(commands))
            if exit_code != 0:
                raise Exception("dvisvgm didn't work\ncommand: %s"%commands)

        return result


class TexMath(Text):
    """Use Tex to render some math"""

    def __init__(self,text=None,pen=None):

        pre = "\\begin{align*} "
        post = " \\end{align*}"
        super().__init__(text,pen=pen,pre=pre,post=post)



class Number(al.CompositeAnObject):

    def __init__(self,number):

        super().__init__()

        st = 0.05

        self.numbers = {
            "0" : [TexMath("0"), [st,0]],
            "1" : [TexMath("1"), [st,0]],
            "2" : [TexMath("2"), [st,0]],
            "3" : [TexMath("3"), [st,0]],
            "4" : [TexMath("4"), [st,0]],
            "5" : [TexMath("5"), [st,0]],
            "6" : [TexMath("6"), [st,0]],
            "7" : [TexMath("7"), [st,0]],
            "8" : [TexMath("8"), [st,0]],
            "9" : [TexMath("9"), [st,0]],
            "." : [TexMath("."), [st+.05,-.16]],
            "-" : [TexMath("-"), [st,0]] }

        self.update(number)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self,value):
        self.update(value)

    def update(self,number):
        self._value=number

        self.clear()

        pos = np.array([0.0,0.0])
        x_pos = 0.0
        y_pos = 0.0
        for digit in str(number):

            glyph = cp.deepcopy(self.numbers[digit][0])
            kern = self.numbers[digit][1]
            self.add_anobject(glyph)
            glyph.position = [x_pos,y_pos+kern[1]]

            x_pos += glyph.e_right-glyph.e_left+kern[0]

class TextBox(al.CompositeAnObject):

    def __init__(self, text, text_pen=None, border_pen=None):
        """A box with lines of text

        Parameters
        ----------
        text : list of strings
            The strings to display in the box

        text_pen : optional Render.Pen
            The pen to use for rendering text.
            default is the default TextAnObject.Text pen

        border_pen : optional Render.Pen
            The pen to use for drawing the box
            default is white outline with no fill
        """
        super().__init__()

        line_spacing = 1.0
        margin = 0.3
        margin = 0.3
        x_dim = 0

        self._text_opacity = 1.0

        self.num_lines = len(text)

        for line,t in enumerate(text):
            text_mob = Text(t)
            text_mob.about_left()
            text_mob.position = [margin,-margin-(line+line_spacing/2)*line_spacing]
            self.add_anobject(text_mob,"line%d"%(line))

            if x_dim < text_mob.e_width:
                x_dim = text_mob.e_width

        x_dim += 2*margin
        y_dim = len(text)*line_spacing+2*margin
        box = al.Rectangle([x_dim,y_dim])
        box.about_upper()
        box.about_left()
        box.position = [0,0]

        self.add_anobject(box)
        self.about_center()
        self.position = [0,0]

    @property
    def text_opacity(self):
        return self._text_opacity;

    @text_opacity.setter
    def text_opacity(self,opacity):
        self._text_opacity = opacity

        for line in range(self.num_lines):
            mob = self.get_anobject("line%d"%line)
            mob.opacity = opacity

