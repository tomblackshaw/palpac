# -*- coding: utf-8 -*-
"""my.globals

Created on May 19, 2024

@author: Tom Blackshaw

This module demonstrates documentation. Docstrings may extend over multiple lines. Sections are created
with a section header and a colon followed by a block of indented text.

Example:
    Examples can be given using either the ``Example`` or ``Examples``
    sections. Sections support any reStructuredText formatting, including
    literal blocks::

        $ python example_google.py

Section breaks are created by resuming unindented text. Section breaks
are also implicitly created anytime a new section starts.

Attributes:
    module_level_variable1 (int): Module level variables may be documented in
        either the ``Attributes`` section of the module docstring, or in an
        inline docstring immediately following the variable.

        Either form is acceptable, but the two should not be mixed. Choose
        one convention to document module level variables and be consistent
        with it.

Todo:
    * For module TODOs
    * You have to also use ``sphinx.ext.todo`` extension

.. _Style Guide:
    https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html

"""

ELEVENLABS_KEY_BASENAME = '.eleven_api_key'  # e.g. /home/foo/.eleven_api_key
MAX_LATLONG_TIMEOUT = 999
DEFAULT_LATLONG_URL = 'http://cqcounter.com/whois/my_ip_address.php'

