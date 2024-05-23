# -*- coding: utf-8 -*-
""" test.randomquoteclass

Created on May 21, 2024

@author: Tom Blackshaw

TODO: WRITE ME
This module demonstrates documentation as specified by the `Google Python
Style Guide`_. Docstrings may extend over multiple lines. Sections are created
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

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

import time

from my.classes.selfcachingcall import SelfCachingCall
from my.exceptions import StillAwaitingCachedValue, WebAPITimeoutError, WebAPIOutputError, WebAPIOverloadError


class _RandomQuoteClass(object):
    # TODO: WRITE ME
    """The summary line for a class docstring should fit on one line.

    If the class has public attributes, they may be documented here
    in an ``Attributes`` section and follow the same formatting as a
    function's ``Args`` section. Alternatively, attributes may be documented
    inline with the attribute's declaration (see __init__ method below).

    Properties created with the ``@property`` decorator should be documented
    in the property's getter method.

    Attributes:
        attr1 (str): Description of `attr1`.
        attr2 (:obj:`int`, optional): Description of `attr2`.

    """
    def __init__(self):
        from my.stringutils import get_random_zenquote
        self._our_zenquote_caching_call = SelfCachingCall(60, get_random_zenquote)
        super().__init__()

    def force_update(self):
        """Forcibly update the currently cached quote."""
        self._our_zenquote_caching_call.update_me()

    @property
    def quote(self):
        # FIXME: these docs are non-standard
        """Obtain a (locally cached) uplifting quote from ZenQuote.

        Using a locally cached copy of the most recent

        Returns:
            str: The resultant quote.

        Raises:
            WebAPITimeoutError: Unable to access website to get quote.
            WebAPIOutputError: Website's output was incomprehensible.
            WebAPIOverloadError: You've overloaded the website, calling it too often.
            StillAwaitingCachedValue: Still waiting for cache to be initialized.

        """
        try:
            the_quote = self._our_zenquote_caching_call.result
            if the_quote.lower().find('zenquotes.io') >= 0:
                raise WebAPIOverloadError("The ZenQuotes website has been called too often (by you). Please wait 2-3 seconds and try again.")
            return the_quote
        except StillAwaitingCachedValue:
            time.sleep(1)
            return self.quote  # FIXME: This is recursion. I don't like recursion.
        except TimeoutError as e:
            raise WebAPITimeoutError("The ZenQuotes website timed out") from e
        except WebAPIOutputError:
            raise WebAPIOutputError("The ZenQuotes website returned an incomprehensible output") from e


RandomQuoteSingleton = _RandomQuoteClass()

'''
from my.classes.randomquoteclass import RandomQuoteSingleton as q
q.quote
'''
