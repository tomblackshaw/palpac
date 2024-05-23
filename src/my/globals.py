# -*- coding: utf-8 -*-
"""my.globals

Created on May 19, 2024

@author: Tom Blackshaw

This module contains the single-line constants.

Attributes:
    ELEVENLABS_KEY_BASENAME (str): The path, within the user's home directory,
        to the API key that Eleven Labs uses.
    MAX_LATLONG_TIMEOUT (int): How long is the default timeout for calling
        get_lat_and_long() and waiting for the reply?
    DEFAULT_LATLONG_URL (str): The default URL for finding out our latitude
        and longitude. It is cqcounter usually.

.. _Style Guide:
   https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html

"""

ELEVENLABS_KEY_BASENAME = '.eleven_api_key'  # e.g. /home/foo/.eleven_api_key
MAX_LATLONG_TIMEOUT = 999
DEFAULT_LATLONG_URL = 'http://cqcounter.com/whois/my_ip_address.php'

