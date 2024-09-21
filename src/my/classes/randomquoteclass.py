# -*- coding: utf-8 -*-
""" test.randomquoteclass

Created on May 21, 2024

@author: Tom Blackshaw

This module contains the functions and classes to do with getting one's
hands on an inspirational quote from ZenQuotes, a website that provides
random quotes for people who want to smile and think happy thoughts.

Example:
    Here is how to use it::

        $ python3
        >>> from my.classes.randomquoteclass import RandomQuoteSingleton as q
        >>> q.quote

Section breaks are created by resuming unindented text. Section breaks
are also implicitly created anytime a new section starts.

Attributes:
    RandomQuoteSingleton (_RandomQuoteClass): Singleton to be imported for
        retrieving a quote.

"""

import time

from my.classes.exceptions import StillAwaitingCachedValue, WebAPITimeoutError, WebAPIOutputError, WebAPIOverloadError
from my.classes.selfcachingcall import SelfCachingCall


class _RandomQuoteClass:
    """Return a random quote when asked for one.

    This class wraps around a SelfCachingCall class instance and provides
    a cached quote from ZenQuotes when asked for one.

    Attributes:
        quote (str): Cached quote.

    """
    def __init__(self):
        from my.stringutils import get_random_zenquote
        self._our_zenquote_caching_call = SelfCachingCall(15, get_random_zenquote)
        super().__init__()

    def force_update(self):
        """Forcibly update the currently cached quote."""
        self._our_zenquote_caching_call.update_me()

    @property
    def quote(self):
        """Obtain a (locally cached) uplifting quote from ZenQuote.

        Using a locally cached copy of the most recent quote, return an inspirational
        quote from ZenQuote, the website of inspirational quotes.

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
            return self.quote
        except TimeoutError as e:
            raise WebAPITimeoutError("The ZenQuotes website timed out") from e
        except WebAPIOutputError:
            raise WebAPIOutputError("The ZenQuotes website returned an incomprehensible output") from e


