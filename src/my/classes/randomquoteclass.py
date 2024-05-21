'''
Created on May 21, 2024

@author: Tom Blackshaw
'''
from my.classes.selfcachingcall import SelfCachingCall
from my.exceptions import StillAwaitingCachedValue, WebAPITimeoutError, WebAPIOutputError


class _RandomQuoteClass(object):

    def __init__(self):
        from my.stringutils import get_random_zenquote
        self._our_zenquote_caching_call = SelfCachingCall(300, get_random_zenquote)
        super().__init__()

    def get_random_quote(self, force_update=False):
        # FIXME: these docs are non-standard
        """Obtain a (locally cached) uplifting quote from ZenQuote.

        Using a locally cached copy of the most recent

        Args:
            force_update (bool): If True, force the cache to update.

        Returns:
            str: The resultant quote.

        Raises:
            WebAPITimeoutError: Unable to access website to get quote.
            WebAPIOutputError: Website's output was incomprehensible.
            StillAwaitingCachedValue: Still waiting for cache to be initialized.

        """

    @property
    def weather(self):
        try:
            return self._our_zenquote_caching_call.result
        except StillAwaitingCachedValue:
            self._our_zenquote_caching_call.update_me()
            return self.weather.result
        except TimeoutError as e:
            raise WebAPITimeoutError("The ZenQuotes website timed out") from e
        except WebAPIOutputError:
            raise WebAPIOutputError("The ZenQuotes website returned an incomprehensible output") from e


RandomQuoteSingleton = _RandomQuoteClass()


class MyClass(object):
    '''
    classdocs
    '''

    def __init__(self, params):
        '''
        Constructor
        '''
