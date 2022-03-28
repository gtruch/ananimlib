# -*- coding: utf-8 -*-
"""
"""
import ananimlib as al

class Scene(al.CompositeAnObject):

    def __init__(self, camera):
        """
        """
        super().__init__()

        # Dictionary of anobjects currently in the scene
        self.time = 0.0         # Current animation time
        self.camera = camera
        self.frame_changed = False

    def render(self):
        """Render the scene onto the camera frame

        Parameters
        ----------
        camera : Camera instance
            An instance of the camera object
        """
        if self.frame_changed:
            self.camera.clearFrame()
            
            super().render(self.camera)

            self.frame_changed = False

    @property
    def frame(self):
        return self.camera.rgba_frame

    def bring_to_top(self,key):
        """Move the anobject at key to the top of the z-order"""
        self.frame_changed = True
        self.data.bring_to_top(key)

    def get_anobject(self,key):
        self.frame_changed = True
        if key == "__camera__":
            return self.camera
        return super().get_anobject(key)

