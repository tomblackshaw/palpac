'''
Created on Aug 22, 2024

@author: Tom Blackshaw
'''
#!/usr/bin/python3
'''
create MP3s
mix them @ sofware level
Sing one MP3 file at a time
'''

from functools import partial
from pathlib import Path
from textwrap import wrap
import argparse
import os
import random
import sys

from more_itertools import sliced
from pydub.audio_segment import AudioSegment
import librosa
import librosa.display
import psola

from my.stringutils import generate_random_string
from my.tools.sound.trim import convert_audio_recordings_list_into_an_mp3_file
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as sig
import soundfile as sf


def closest_pitch(f0, the_notes, squelch=0):
    """Round the given pitch values to the nearest MIDI note numbers"""
    midi_note = np.around(librosa.hz_to_midi(f0))
    # To preserve the nan values.
    nan_indices = np.isnan(f0)
    midi_note[nan_indices] = np.nan
    # Convert back to Hz.
    res_dat = librosa.midi_to_hz(midi_note)
    nans_in_a_row = 0
    current_note_number = -1
    for i in range(0, len(res_dat)):
        if np.isnan(res_dat[i]):
            nans_in_a_row += 1
        else:
            if nans_in_a_row >= squelch and current_note_number < len(the_notes) - 1:
                current_note_number += 1
            res_dat[i] = librosa.note_to_hz(the_notes[current_note_number])
            nans_in_a_row = 0
    return res_dat


def autotune(audio, sr, the_notes, squelch):
    # Set some basis parameters.
    frame_length = 2048
    hop_length = frame_length // 4
    fmin = librosa.note_to_hz('C2')
    fmax = librosa.note_to_hz('C7')

    # Pitch tracking using the PYIN algorithm.
    f0, voiced_flag, voiced_probabilities = librosa.pyin(audio,
                                                         frame_length=frame_length,
                                                         hop_length=hop_length,
                                                         sr=sr,
                                                         fmin=fmin,
                                                         fmax=fmax)

    # Apply the chosen adjustment strategy to the pitch.
    corrected_f0 = closest_pitch(f0, the_notes, squelch)

    # Pitch-shifting using the PSOLA algorithm.
    return psola.vocode(audio, sample_rate=int(sr), target_pitch=corrected_f0, fmin=fmin, fmax=fmax)


def autotune_this_mp3(infile, outfile, notes, squelch=0):
    # 'c4 d4 e4 f4 g4 a4 b4 c5'.split(' ')
    # squelch=3
    y, sr = librosa.load(infile, sr=None, mono=False)
    # Only mono-files are handled. If stereo files are supplied, only the first channel is used.
    if y.ndim > 1:
        y = y[0,:]
    # Perform the auto-tuning.
    pitch_corrected_y = autotune(y, sr, the_notes=notes, squelch=squelch)
    sf.write(outfile, pitch_corrected_y, sr)


def save_mp3_audio_of_one_voice_singing_one_phrase(voice, phrase, notes, autotunedfile, squelch):
    from my.text2speech import Text2SpeechSingleton as tts
    tts.voice = voice
    audio = [tts.audio(text=phrase)]
    rndstr = generate_random_string(42)
    exportfile = '/tmp/tts{rndstr}.mp3'.format(rndstr=rndstr)
    convert_audio_recordings_list_into_an_mp3_file(audio, exportfile)
    autotune_this_mp3(exportfile, autotunedfile, notes, squelch=squelch)
    os.unlink(exportfile)


def save_mp3_audio_of_several_voices_singing_one_phrase(voices_list, phrase, notes, outputfile, squelch):
    fnames_list = []
    fnameroot = '/tmp/tts%s' % generate_random_string(32)
    noof_voices = 0
    for voice in voices_list:
        out_fname = '{fnameroot}.{i}.mp3'.format(fnameroot=fnameroot, i=noof_voices)
#        print('notes =', notes[noof_voices])
        save_mp3_audio_of_one_voice_singing_one_phrase(voice, phrase, notes[noof_voices], out_fname, squelch)
        fnames_list.append(out_fname)
        noof_voices += 1
    all_sounds = [AudioSegment.from_file(fnames_list[i], format='mp3') for i in range(noof_voices)]
    cumulative_overlay = all_sounds[0]
    for i in range(1, noof_voices):
        cumulative_overlay = cumulative_overlay .overlay(all_sounds[i])
    cumulative_overlay.export(outputfile, format="mp3")
    for f in fnames_list:
        os.unlink(f)


def save_mp3_audio_of_several_voices_singing_several_phrases(voices_list, phrases_and_notes_lst, outputfile, squelch=1, trim_level=1):
    # generate a combined audio for for each phrase; then, concatenate them all
    fnames_list = []
    fnameroot = '/tmp/tts%s' % generate_random_string(32)
    for phraseno in range(len(phrases_and_notes_lst)):
        # generate a choir sound for ONE PHRASE
        phrase, notes = phrases_and_notes_lst[phraseno]
        outmp3f = '{fnameroot}.{phraseno}.mp3'.format(fnameroot=fnameroot, phraseno=phraseno)
        save_mp3_audio_of_several_voices_singing_one_phrase(voices_list, phrase, notes, outmp3f, squelch)
        fnames_list.append(outmp3f)
    all_sounds = [open(fnam, "rb").read() for fnam in fnames_list]  # AudioSegment.from_file(fnam, format='mp3')
    convert_audio_recordings_list_into_an_mp3_file(all_sounds, outputfile, trim_level=trim_level)
    for f in fnames_list:
        os.unlink(f)


def make_the_monks_chant(voices, phrases, chords, outfile, squelch):
    lst = []
    for phraseno in range(0, len(phrases)):
        phrase = phrases[phraseno]
        chord = chords[phraseno]
#        print("Working on", phrase)
        lst.append([phrase, [[random.choice(chord)] for _ in voices]])
    save_mp3_audio_of_several_voices_singing_several_phrases(voices, lst, outfile, squelch)

