'''
Created on Aug 17, 2024

@author: Tom Blackshaw


0 0
1 51
2 60
3 68
4 75
5 81
6 86
7 90
8 93
9 95
10 96
11 100
'''

#if __name__ == '__main__':
#    pass


import os
import sys

# from my.classes.text2speechclass import convert_audio_recordings_list_into_an_mp3_file
# from my.stringutils import convert_24h_and_mins_to_shorttime

# def speak_from_cache(voice, phrases):
#     from my.text2speech import Text2SpeechSingleton as tts
#     data = []
#     tts.voice = voice
#     for txt in phrases:
#         data.append(get_cached_audio_for_phrase(tts.voice, txt))
#     convert_audio_recordings_list_into_an_mp3_file(data, 'out.mp3', trim_level=1)
#     os.system("mpv out.mp3")




if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("cachespeech <voice> <text> <outfile>")
        sys.exit(1)
    the_voice, the_text, outfile = sys.argv[1:4]
    audio_data = phrase_audio(the_voice, the_text)
    with open(outfile, 'wb') as f:
        f.write(audio_data)
    sys.exit(0)

