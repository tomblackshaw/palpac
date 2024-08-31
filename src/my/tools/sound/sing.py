#!/usr/bin/python3

'''
Created on Aug 22, 2024

@author: Tom Blackshaw

create MP3s
mix them @ sofware level
Sing one MP3 file at a time

    sing_a_random_alarm_message(owner='Charlie', voice=this_voice, hour=datetime.datetime.now().hour, minute=datetime.datetime.now().minute, snoozed=False,
                                len_per=7, keys=[Cmaj, Fmaj, Gmaj, Fmaj, Fmin, Cmaj])

    songify_this_mp3(infile='audio/cache/Sarah/charlie..mp3', outfile='/tmp/00.mp3', noof_singers=1,
                         keys=[['c4'.split(' ')]], len_per=4, squelch=3)
    songify_this_mp3(infile='audio/cache/Sarah/charlie?.mp3', outfile='/tmp/01.mp3', noof_singers=1,
                         keys=[['g4'.split(' ')]], len_per=4, squelch=3)
    songify_this_mp3(infile='audio/cache/Sarah/charlie!.mp3', outfile='/tmp/02.mp3', noof_singers=1,
                         keys=[['c5'.split(' ')]], len_per=4, squelch=3)
    songify_this_mp3(infile='audio/cache/Sarah/you_really_should_get_up,.mp3', outfile='/tmp/03.mp3', noof_singers=3,
                         keys=['g3 c4 e4 g4 c5 e5 c6'.split(' '), 'c3 g3 c4 d#4 g4 c5 d#5 c6'.split(' '), ], len_per=1, squelch=3)
    songify_this_mp3(infile='audio/cache/Sarah/up_you_get!.mp3', outfile='/tmp/04.mp3', noof_singers=1,
                         keys=[['c4'.split(' ')]], len_per=4, squelch=3)
    songify_this_mp3(infile='audio/cache/Sarah/up_you_get!.mp3', outfile='/tmp/05.mp3', noof_singers=1,
                         keys=[['g4'.split(' ')]], len_per=4, squelch=3)
    songify_this_mp3(infile='audio/cache/Sarah/up_you_get!.mp3', outfile='/tmp/06.mp3', noof_singers=1,
                         keys=[['c5'.split(' ')]], len_per=4, squelch=3)
    songify_this_mp3(infile='audio/cache/Sarah/you_really_should_get_up,.mp3', outfile='/tmp/07.mp3', noof_singers=3,
                         keys=['g3 c4 d#4 g4 c5 d#5 c6'.split(' '), 'c3 g3 c4 e4 g4 c5 e5 c6'.split(' '), ], len_per=1, squelch=3)


'''

from functools import partial
from pathlib import Path
from textwrap import wrap
import argparse
import datetime
import os
import random
import sys

from more_itertools import sliced
from pydub.audio_segment import AudioSegment
import librosa
import librosa.display
import psola

from my.consts import Cmaj
from my.stringutils import generate_random_string, generate_random_alarm_message
from my.tools.sound.trim import convert_audio_recordings_list_into_an_mp3_file
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as sig
import soundfile as sf


def closest_pitch(f0, the_notes, squelch=0):
    """Round the given pitch values to the nearest MIDI note numbers"""
    # FIXME WRITE DOX
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
    # FIXME WRITE DOX
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
    # FIXME WRITE DOX
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
    # FIXME WRITE DOX
    from my.text2speech import Text2SpeechSingleton as tts
    tts.voice = voice
    audio = [tts.audio(text=phrase)]
    rndstr = generate_random_string(42)
    exportfile = '/tmp/tts{rndstr}.mp3'.format(rndstr=rndstr)
    convert_audio_recordings_list_into_an_mp3_file(audio, exportfile)
    autotune_this_mp3(exportfile, autotunedfile, notes, squelch=squelch)
    os.unlink(exportfile)


def save_mp3_audio_of_several_voices_singing_one_phrase(voices_list, phrase, notes, outputfile, squelch):
    # FIXME WRITE DOX
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
    # FIXME WRITE DOX
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
    # FIXME WRITE DOX
    lst = []
    for phraseno in range(0, len(phrases)):
        phrase = phrases[phraseno]
        chord = chords[phraseno]
#        print("Working on", phrase)
        lst.append([phrase, [[random.choice(chord)] for _ in voices]])
    save_mp3_audio_of_several_voices_singing_several_phrases(voices, lst, outfile, squelch)


def this_voice_note_sequences(keys, len_per, voxno):
    # FIXME WRITE DOX
    notes = []
    for k in keys:
        notes += [k[voxno] for _ in range(len_per)]
    return notes


def songify_this_mp3(infile, outfile, noof_singers, keys, len_per, squelch):
    # FIXME WRITE DOX
    rndstr = generate_random_string(32)
    temp_fname = '/tmp/tts{rndstr}.autotuned.mp3'.format(rndstr=rndstr)
    all_sounds = []
    for i in range(noof_singers):
        if len(keys) > noof_singers:
            notes = randomized_note_sequences(keys=keys, len_per=len_per)
        else:
            notes = this_voice_note_sequences(keys=keys, len_per=len_per, voxno=i)
        autotune_this_mp3(infile, temp_fname, notes, squelch=squelch)
        all_sounds.append(AudioSegment.from_file(temp_fname, format="mp3"))
    cumulative_overlay = all_sounds[0]
    for i in range(1, len(all_sounds)):
        cumulative_overlay = cumulative_overlay.overlay(all_sounds[i])
    cumulative_overlay.export(outfile , format="mp3")
    os.unlink(temp_fname)


def randomized_note_sequences(keys, len_per):
    # FIXME WRITE DOX
    notes = []
    for k in keys:
        notes += [random.choice(k) for _ in range(len_per)]
    return notes
# make_the_monks_chant(('Callum', 'Laura', 'Charlotte', 'Alice'), 'Today is my birthday. I am happy.'.split(' '), \
#                      (Cmaj, Cmaj, Gmaj, Fmaj, Fmaj, Fmin, Cmaj),
#                      '/tmp/out.mp3', squelch=5)
#    sys.exit(0)




