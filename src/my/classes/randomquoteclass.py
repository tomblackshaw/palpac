'''
Created on May 21, 2024

@author: Tom Blackshaw


'''
import time

from my.classes.selfcachingcall import SelfCachingCall
from my.exceptions import StillAwaitingCachedValue, WebAPITimeoutError, WebAPIOutputError, WebAPIOverloadError


class _RandomQuoteClass(object):

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
