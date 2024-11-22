# -*- coding: utf-8 -*-
"""my.globals

Created on May 19, 2024

@author: Tom Blackshaw

This module contains the single-line constants.

Attributes:
    ELEVENLABS_KEY_BASENAME (str): The path, within the user's home directory,
        to the API key that Eleven Labs uses.

.. _Style Guide:
   https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html

"""
import os

# def where_is_binary(binary_name):
#     try:
#         return ['%s/%s'%(mydir, binary_name) for mydir in sys.path+['/opt/homebrew/bin','/usr/bin','/usr/local/bin','/usr/sbin','/usr/local/sbin'] if os.path.exists('%s/%s'%(mydir, binary_name))][0]
#     except IndexError as e:
#         raise FileNotFoundError(e)

ELEVENLABS_KEY_FILENAME = '%s%s%s' % (os.path.expanduser('~'), os.sep, '.eleven_api_key')  # e.g. /home/foo/.eleven_api_key
SOUNDS_CACHE_PATH = 'sounds/cache'
SOUNDS_ALARMS_PATH = 'sounds/alarms'
TRIMMED_ALARMS_PATH = 'sounds/trimmedalarms'
SOUNDS_FARTS_PATH = 'sounds/farts'
LAZY_SILENCE_THRESHOLD = -65.0
DEFAULT_SILENCE_THRESHOLD = -50.0
SNIPPY_SILENCE_THRESHOLD = -30.0
_faces_dct = {  # 'neon 1':'ui/clocks/neon-clock-css-jquery/dist/index.html',
#             'neon 2':'ui/clocks/this-neon/dist/index.html',
             'braun':'ui/clocks/braun-clock/dist/index.html',
             'analog 1':'ui/clocks/analog-clock-1/dist/index.html',
             'analog 2':'ui/clocks/analog-digital-clock/dist/index.html',
             'digital 1':'ui/clocks/digital-clock-1/dist/index.html',
             'digital 2': 'ui/clocks/digital-clock-2/dist/index.html',
             'clean': 'ui/clocks/minimal-clean-analog/index.html',
             'simple': 'ui/clocks/simple_javascript_clock/dist/index.html',
             'wall':'ui/clocks/wall-clock/dist/index.html',
             'rounded':'ui/clocks/rounded-clock-main/index.html',
             'series 2':'ui/clocks/time-series-2-typographic-clock/dist/index.html',
#             '3D':'ui/clocks/3d-clock/dist/index.html',
             'slide':'ui/clocks/slide-clock/dist/index.html',
             'challenge':'ui/clocks/dev-challenge-week-3/dist/index.html',
             'another':'ui/clocks/another-canvas-clock/dist/index.html',
             'reddy':'ui/clocks/reddy-clock/index.html',
    }
PATHNAMES_OF_CLOCKFACES = [_faces_dct[k] for k in _faces_dct]
ZOOMS_DCT = {  # _faces_dct['neon 1']:.9,
#              _faces_dct['neon 2']:1.16,
              _faces_dct['analog 1']:1.46,
              _faces_dct['simple']:1.75,
              _faces_dct['another']:0.93,
              _faces_dct['digital 1']:1.1,
#              _faces_dct['3D']:1.5,
              _faces_dct['braun']:1.3,
              }

TOUCHSCREEN_SIZE_X, TOUCHSCREEN_SIZE_Y = 480, 480

