# -*- coding: utf-8 -*-
"""
Customizable configuration objects
"""

class Config(dict):
    """Config base class

    Allows access of configuration parameters using either dictionary keys
    or as attributes of the config object using dot notation.
    """

    def __init__(self,defaults, iniSettings):
        """Ingest configuration Settings

        Parameters
        ----------
        defaults : dict
            Hard coded default values and associated data type.
            Inclusion of the type information allows on the fly
            type conversion as data is read from the ini file.

            Entries are constructed as:

                { setting_name : {'value': val, 'dtype': type} }

        iniSettings : dict
            Incoming configuration Settings in simple key: value pairs.
            Type converted according to type information in default dict.
        """

        self.defaults = defaults

        # Ingest the defaults
        for k,d in defaults.items():
            self[k] = d['value']

        # Ingest additional settings
        self.reconfigure(iniSettings)

    def reconfigure(self,settings,convert_types=True):
        """Ingest additional configuration settings

        If settings in the dictionary are from an ini file, the dictionary
        values may be strings.  In that case, they are type converted based on
        the type information in the defaults dict

        Parameters
        ----------
        settings : dict
            Incoming configuration Settings in simple key: value pairs.
            Type converted according to type information in default dict.

        convert_types : optional bool
            If True, types are converted.
            If False, types are left as they are
            default = True
        """

        # Ingest any additonal settings and perform type conversion
        # on known parameters.
        for k,d in settings.items():
            self[k] = d

        if convert_types:
            self._convert_types()

    def _convert_types(self):
        """Scan internal dictionary and convert types for known keys

        Known keys are those stored in self.defaults along with their
        associated type information.

        All data read from an ini file is initially of type str
        """

        for k,v in self.items():

            # 'None' values from the ini file
            if v == 'None':
                self[k] = None

            elif k in self.defaults.keys():
                dtype = self.defaults[k]['dtype']      # Fetch the type

                # Have to treat bools differently
                if dtype is bool:
                    self[k] = (v == 'True')
                else:
                    self[k] = dtype(v)            # Perform explicit conversion

    def __getattr__(self,attr):
        """Allows the use of dot notation to get dict entries"""
        return self[attr]

    def __setattr__(self,attr,value):
        """Allows the use of dot notation to set dict entries"""
        self[attr] = value


class CameraConfig(Config):
    """Configuration settings for the camera module

    Attributes
    ----------
    pixel_height, pixel_width : int
        Dimensions of the camera window in pixels

    frame_height, frame_width : float
        Dimensions of the Scene contained within the camera window
        in Scene Units

    camera_x_center, camera_y_center : float
        Position of the center of the camera window in Scene Coordinates

    camera_rotation : float
        The camera rotation angle in radians

    frame_rate : int
        Animation speed in frames per second
    """

    def __init__(self, iniSettings={}):
        self.high_quality = {
            "pixel_height": 1080,
            "pixel_width": 1920,
            "frame_rate": 60,
        }

        self.medium_quality = {
            "pixel_height": 720,
            "pixel_width": 1280,
            "frame_rate": 30,
        }

        self.low_quality = {
            "pixel_height": 480,
            "pixel_width": 854,
            "frame_rate": 15,
        }

        defaults = {
         'pixel_height'    : { 'value': 1080,   'dtype': int },
         'pixel_width'     : { 'value': 1920,   'dtype': int },
         'frame_height'    : { 'value': 8.0,    'dtype': float },
         'frame_width'     : { 'value': "None", 'dtype': float },
         'camera_x_center' : { 'value': 0.0,    'dtype': float },
         'camera_y_center' : { 'value': 0.0,    'dtype': float },
         'camera_rotation' : { 'value': 0.0,    'dtype': float },
         'frame_rate'      : { 'value': 60,     'dtype': int }
        }

        super().__init__(defaults, iniSettings)
        self._fixAspectRatio()

    def _fixAspectRatio(self):

        # Maintain aspect ratio between pixel and frame coordinates
        # Unless a specific frame width is specified
        if self.frame_width is None:
            self.frame_width = (self.frame_height *
                                self.pixel_width / self.pixel_height)


    def setHighQuality(self):
        self.reconfigure(self.high_quality)
        self.frame_width = None
        self._fixAspectRatio()

    def setMediumQuality(self):
        self.reconfigure(self.medium_quality)
        self.frame_width = None
        self._fixAspectRatio()

    def setLowQuality(self):
        self.reconfigure(self.low_quality)
        self.frame_width = None
        self._fixAspectRatio()

class FileWriterConfig(Config):
    """Configuration settins for File Writer

    Attributes
    ----------
    save_last_frame : Boolean
        default = False

    save_pngs : Boolean
        default = False

    save_as_gif : Boolean
        default = False

    png_mode : String
        default = 'RGB'

    movie_file_extension : String
        default = '.mp4'

    file_name : String
        default = None

    input_file_path : Striug
        default = '.\\'
    """

    def __init__(self, iniSettings):
        defaults = {
          'write_to_movie': { 'value': True, 'dtype': bool},
          'save_last_frame': { 'value': False, 'dtype': bool},
          'save_pngs': { 'value': False, 'dtype': bool },
          'save_as_gif': { 'value': False, 'dtype': bool },
          'png_mode': { 'value': 'RGB', 'dtype': str },
          'movie_file_extension': { 'value': '.mp4', 'dtype': str },
          'file_name': { 'value': "None", 'dtype': str },
          'input_file_path': { 'value': '.\\', 'dtype':  str },
        }

        super().__init__(defaults, iniSettings)


class SceneConfig(Config):
    """Configuration settings for Scene

    Attributes
    ----------
    skip_animations : Boolean
        default = False

    start_at_animation_number : Int
        default = None

    end_at_animation_number : Int
        default = None

    leave_progress_bars : Boolean
        default = False
    """

    def __init__(self, iniSettings):
        defaults = {
            "skip_animations" : { 'value': False, 'dtype': bool },
            "start_at_animation_number" : { 'value': "None", 'dtype': int },
            "end_at_animation_number" : { 'value': "None", 'dtype': int },
            "leave_progress_bars" : { 'value': False, 'dtype': bool }
        }


        super().__init__(defaults, iniSettings)


class DirectoryConfig(Config):
    """Output Directory configuration settings

    Attributes
    ----------
    media_dir : String
        Base directory for all media files
        default = None

    video_dir : String
        Subdirectory for output video files
        default = None

    video_output_dir : String
        Additional name for video_dir?
        default = None

    tex_dir : String
        Subdirectory for output tex files
        default = None
    """
    def __init__(self, iniSettings):
        defaults = {
         'media_dir': { 'value': './', 'dtype': str },
         'video_dir': { 'value': './video', 'dtype': str },
         'video_output_dir': { 'value': './video', 'dtype': str },
         'tex_dir': { 'value': './tex', 'dtype': str },
         'quiet': { 'value': False, 'dtype': bool },
         'open_video_upon_completion': { 'value': False, 'dtype': bool },
         'show_file_in_finder': { 'value': False, 'dtype': bool }
        }

        super().__init__(defaults, iniSettings)

class AbaondonedConfig(Config):

    def __init__(self, iniSettings):

        defaults = {
         'ignore_waits': { 'value': True, 'dtype': bool },
         'write_all': { 'value': False, 'dtype': bool },
         'sound': { 'value': False, 'dtype': bool }
        }

        super().__init__(defaults, iniSettings)


