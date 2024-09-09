# -*- coding: utf-8 -*-
"""my.tools

Created on May 19, 2024

@author: Tom Blackshaw

This module contains GUI-related tools.

.. _Style Guide:
   https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html

"""

import os
from my.classes.exceptions import PyQtUICompilerError


def set_vdu_brightness(brightness):
    # Technically, brightness>100 will be ignored by the hardware.
    if type(brightness) is not int:
        raise TypeError("Brightness parameter must be an integer")
    elif brightness < 0 or brightness > 100:
        raise ValueError("Brightness parameter must be between 0 and 100 (inclusive)")
    # echo {onoroff} > /sys/class/backlight/rpi_backlight/brightness; \
    res = os.system('''gpio -g mode 19 pwm; gpio -g pwm 19 {brightness}'''.format(brightness=brightness * 10))
    return res


def set_audio_volume(volume, mixer="Master"):
    """Set the volume of the principal ALSA device.

    Args:
        v (int): Volume level, from 0 to 11. (Don't use 11.)

    Raises:
        ValueError: if v<0 or >11
        TypeError: if v is not int.
    """
    real_vol_list = [0, 51, 60, 68, 75, 81, 86, 90, 93, 95, 96, 100]
    if type(volume) is not int:
        raise TypeError("set_audio_volume() takes an integer parameter, please.")
    if volume < 0 or volume > 11:
        raise ValueError("set_audio_volume() takes an int between 0 and 10, inclusive, please.")
    os.system('''amixer set "{mixer}" {volume}%'''.format(mixer=mixer, volume=real_vol_list[volume]))


def compile_all_uic_files(a_path):
    """Compile the UIC files in the supplied path.

    Using the PyQt-supplied UIC file compiler, turn the path's every UIC file
    into a set of importable Python modules/wrappers.

    Args:
        a_path (str): Path to the directory.

    Returns:
        n/a

    """
    from os import listdir
    from os.path import isfile, join
    onlyfiles = [f for f in listdir(a_path) if isfile(join(a_path, f))]
    for f in onlyfiles:
        if f.endswith('.ui'):
            cmd = '''pyuic5 -o "{a_path}/{pyfile}" "{a_path}/{uifile}"'''.format(
                a_path=a_path,
                uifile=f,
                pyfile=f[:-2] + 'py')
            if 0 != os.system(cmd):
                raise PyQtUICompilerError("{cmd} failed".format(cmd=cmd))
