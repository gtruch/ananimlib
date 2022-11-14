# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 12:53:16 2019

@author: G. Ruch
"""
import os
import os.path
import subprocess
import numpy  as np
import copy   as cp

# Disable pygame support prompt
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "True"
import pygame as pg
from   PIL import Image

class Backend():    
    """Default backend - Buffers frames in memory

    Attributes
    ----------
    width : float
        width of a frame in pixels
        
    height : float
        height of the frame in pixels
    """

    def __init__(self,width,height,frame_rate):

        # Set scale and offset
        self.frameSize = np.array([width,height],dtype=int)
        self.frame_rate = frame_rate


        # Initialize pygame
#        pg.init()


        self.frames = []

    @property
    def frame_rate(self):
        return self._frame_rate

    @frame_rate.setter
    def frame_rate(self,rate):
        self._frame_rate = rate
        if rate == 1:
            print("Hey! That stings.")

    def start(self):
        """Nothing to do here... """
        pass

    def addFrame(self,frame):
        """Stores an RGBA frame."""
        
        self.frames.append(frame)            
#        self.frames.append(cp.copy(np.transpose(frame[:,:,:3],[1,0,2])))
        
        
    def save_frame(self,fname,frame_number=0):
        pass
    
    def save_mp4(self,fname):
        """Save the animation as an mp4"""
        
        mp4_writer = MP4Backend(self.frameSize[0],self.frameSize[1],
                                self.frame_rate, fname)
        
        mp4_writer.frames=self.frames
        mp4_writer.end()
        

        
    def save_gif(self,fname):
        """Save the animation as a GIF
        
        The frame delay is limited to an integer number of milliseconds by 
        the GIF specification.  For the animation to appear as expected, 
        set the frame rate to one of the followign
        -    100  (1 millisecond delay)
        -    50   (2 millisecond delay)
        -    33.3 (3 millisecond delay)
        -    25   (4 millisecond delay)
        -    etc... 
            
        If a different frame rate is used, the closest possible integer delay 
        will be selected as round(100/frame_rate)
        """
        print("save_gif entered")
        # Convert the frames to a list of PIL images
        images = [Image.fromarray(f) for f in self.frames]
        
        # Write the images to a gif
        print(f"Saving: {fname}")
        images[0].save(fname,"GIF",save_all=True,
                       append_images=images[1:], loop=0,optimize=False,disposal=1,
                       duration = int(np.round(1000/self.frame_rate)))


    def end(self):
        return
        # if len(self.frames) > 0:
        #     self.play_movie()

    def play_movie(self,repeat=-1):

        # initialize the display
        pg.display.init()
        screen = pg.display.set_mode(self.frameSize)
        done = False
        frameNum = 0
    

        # Calculate time between frames in milliseconds
        frameTime = (1/self.frame_rate)*1e3


        # Clear any queued events before starting the playback.
        pg.event.clear()
        while not done:   # Some event triggers done
            start_time = pg.time.get_ticks()

            #display a frame
            frame = self.frames[frameNum]
            pg.surfarray.blit_array(screen,np.transpose(frame[:,:,:3],[1,0,2]))

            #    screen.blit(s,s.get_rect())
            pg.display.flip()
            frameNum += 1
            if frameNum >= len(self.frames):
                if repeat != 0:
                    frameNum=0
                if repeat == 0:
                    done = True
                elif repeat > 0:
                    repeat -= 1

            # Pause for one frame time
            time = pg.time.get_ticks()
            pg.time.wait(int(np.round(frameTime-(time-start_time))))

            # Handle Events.
            for event in pg.event.get():

                if event.type == pg.QUIT:
                    done = True

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        done = True

        pg.display.quit()
 

    def __del__(self):
        pg.quit()



class MP4Backend():
    """Use ffmpeg to write mp4s adapted from manimlib.scene.scenefilewriter
    """

    def __init__(self,pixel_width,pixel_height,frame_rate,
                  outName,outDir="./",showVideo=False):
        """Get ready to write mp4s!

        Parameters
        ----------
        outName : str
            The base name of the output file.

        pixel_width, pixel_height : Int
            The dimensions of incoming frames in pixels.
            Note: Dimensions must be divisible by 2.

        frame_rate : Int
            The desired frame of the final video in frames per second

        outDir : optional, str
            The output path.
            default = './'

        """
        self.outName = outName
        self.outDir = outDir
        self.frameSize = np.array([pixel_width,pixel_height])
        self.frame_rate = frame_rate

        if not os.path.exists(self.outDir):
            os.makedirs(self.outDir)

        self.frames=[]

    def start(self):
        pass

    def addFrame(self,frame):
        """buffer the frame"""
        self.frames.append(cp.copy(frame))


    def end(self):
        """Open a pipe to ffmpeg"""
        writing_process = self._open_movie_pipe()

        for frame in self.frames:
            # try:
            writing_process.stdin.write(frame.tobytes())
            # except:
            #     out = writing_process.communicate()
            #     print("out")

        self.close_movie_pipe(writing_process)
        self.frames=[]

    def _open_movie_pipe(self):

        if not os.path.exists(self.outDir):
            os.makedirs(self.outDir)

        # Ensure that the outName doesn't have a path or extension
        fname = os.path.split(self.outName)[1]
        fname = os.path.splitext(fname)[0]
        file_path = os.path.join(self.outDir,fname+'.mp4')


        command = [
            'ffmpeg',
            '-y',  # overwrite output file if it exists
            '-f', 'rawvideo',
            '-s', '%dx%d' % (self.frameSize[0], self.frameSize[1]),
            '-pix_fmt', 'rgba',
            '-r', str(self.frame_rate),  # frames per second
            '-i', '-',  # The imput comes from a pipe
            '-c:v', 'h264_nvenc',
            '-an',  # Tells FFMPEG not to expect any audio
            '-loglevel', 'verbose',
            '-vcodec', 'libx264',
            '-pix_fmt', 'yuv420p',
            file_path
        ]

        # Note: For debugging, add stderr=subprocess.PIPE to the line below
        # Then read output from subprocess with subprocess.communicate()
        proc = subprocess.Popen(command,
                                stdin=subprocess.PIPE,
                                stdout=subprocess.DEVNULL,
                                stderr=subprocess.STDOUT
#                                stderr=subprocess.PIPE
        )


#        out = proc.communicate()

        return proc

    def play_movie(self, *args):
        pass

    def close_movie_pipe(self,pipe):
        pipe.stdin.close()
        pipe.wait()














