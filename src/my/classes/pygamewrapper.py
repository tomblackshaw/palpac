'''
Created on Oct 13, 2024

@author: mchobbit
'''

# import pygame  # @UnresolvedImport
#
# class _PyGameWrapperClass:
#     '''
#     Provide rotating cache of N channels, each for a different phrase to be spoken.
#     '''
#     def __init__(self):
#         self.cache_size = 10 # FIXME: Increase to 100, eventually.
#         pygame.mixer.init()
#         self.fnames_lst = [None]*self.cache_size
#         self.sounds_lst = [None]*self.cache_size
#         self.cache_pointer = 0
#
#     def add_item_to_cache(self, fname):
#         self.fnames_lst[self.cache_pointer] = fname
#         self.sounds_lst[self.cache_pointer] = pygame.mixer.Sound(fname)
#         self.cache_pointer = (self.cache_pointer+1) % self.noof_channels
#
#     def play(self, fname):
#         if fname not in self.fnames_lst:
#             self.add_item_to_cache(fname)
#         pygame.mixer.find_channel().play(self.sounds_lst[self.fnames_lst.index(fname)])
#         while pygame.mixer.music.get_busy() == True:
#             continue