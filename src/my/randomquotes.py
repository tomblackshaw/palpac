# -*- coding: utf-8 -*-
"""Creates singleton for _RandomQuoteClass

Created on May 24, 2024

@author: Tom Blackshaw

Attributes:
    RandomQuoteSingleton
        .force_update()
        .quote             latest quote (string)

Notes:
    A new quote is downloaded periodically from the Internet.
    This subroutine will not work unless you are online.
    
.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

from my.classes.randomquoteclass import _RandomQuoteClass

RandomQuoteSingleton = _RandomQuoteClass()
