#!/usr/bin/python3

'''
Created on Aug 17, 2024
Updated on Nov 05, 2024

@author: Tom Blackshaw
'''

import sys
from my.text2speech import phrase_audio

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("cachespeech <voice> <text> <outfile>")
        sys.exit(1)
    the_voice, the_text, outfile = sys.argv[1:4]
    audio_data = phrase_audio(the_voice, the_text, suffix='mp3')
    with open(outfile, 'wb') as f:
        f.write(audio_data)
    sys.exit(0)
