# -*- coding: utf-8 -*-
"""Tools to trim the silence from either end of audio files.

Created on Aug 21, 2024
Updated on Nov 05, 2024

@author: Tom Blackshaw

This module contains functions that trim silence from either end of audio samples,
concatenate audio recordings, and so on. Technically, I'm not sure why it should
be called 'trim' as opposed to 'trim_and_concat', but that's okay. No one is perfect.

Examples:
    TODO writeme

Todo:
    * Write examples

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

import os

from pydub.audio_segment import AudioSegment

from my.globals import DEFAULT_SILENCE_THRESHOLD, SNIPPY_SILENCE_THRESHOLD, LAZY_SILENCE_THRESHOLD
from my.stringutils import generate_random_string


def detect_leading_silence(sound:AudioSegment, silence_threshold:float=DEFAULT_SILENCE_THRESHOLD, chunk_size:int=10) -> int:
    """Detect the leading silence in a sound sample.

    If there's silence at the start of the sound sample, find it. Iterate over\
    chunks until you find the first one with sound

    Args:
        sound: The audio data.
        silence_threshold: The silence threshold, for 'squelching', in decibels.
        chunk_size: How many milliseconds should we examine at a time.

    Returns:
        int: Number of milliseconds of leading silence that we found.

    Raises:
        Unknown.

    """
    trim_ms = 0  # ms
    assert chunk_size > 0  # to avoid infinite loop
    while sound[trim_ms:trim_ms + chunk_size].dBFS < silence_threshold and trim_ms < len(sound):
        trim_ms += chunk_size
    return trim_ms


def convert_audio_recordings_list_into_one_audio_recording(data, trim_level, suffix) -> AudioSegment:
    """Convert a list of audio data into one AudioSegment instance.

    Write the supplied list of data (probably MP3) to individual files.
    Use the pydub library to combine them into a single AudioSegment
    instance.

    Args:
        data: The list of MP3 data. I say 'list' because
            this is a *list* of several bytes, not several *bytes*. To
            access MP3 data #0, read data[0]. That's the first MP3 file.
            The second is data[1]. You get the picture, I hope.
        trim_level: If 0, don't trim. If 1, trim. If 2, trim aggressively.
        suffix: mp3 or ogg

    Returns:
        AudioSegment: An instance of an AudioSegment, ready to be exported
            etc. via the 'export' method: AudioSegment.export

    Raises:
        Unknown.

    """
    sounds = None
    # We use MP3 here. It doesn't matter why. We delete the file in the end anyway.
    filenames = ''
    for d in data:
        fname = '/tmp/{rnd}.{suffix}'.format(rnd=generate_random_string(32), suffix=suffix)
        filenames += ' {fname}'.format(fname=fname)
        with open(fname, 'wb') as f:
            f.write(d)
            untrimmed_audio = AudioSegment.from_mp3(fname) if suffix == 'mp3' \
                            else AudioSegment.from_ogg(fname) if suffix == 'ogg' \
                            else AudioSegment.from_file(fname)
        trimmed_aud = trim_my_audio(untrimmed_audio, trim_level)
        if sounds is None:
            sounds = trimmed_aud
        else:
            sounds += trimmed_aud
    if sounds is not None:
        for fname in filenames.strip(' ').split(' '):
            assert(fname[0] == '/')
            os.unlink(fname)
    return sounds


def trim_my_audio(untrimmed_audio:AudioSegment, trim_level:int) -> AudioSegment:
    """Trim the suppiled audio.

    If there's silence at the start and/or end of the sound sample, trim it off.

    Args:
        untrimmed_audio: The untrimmed audio data.
        trim_level: How much trimming should we do?
            0=nearly none; 1=normal; 2=aggressive.

    Returns:
        AudioSegment: Trimmed audio.

    Raises:
        Unknown.

    """

    silence_threshold = SNIPPY_SILENCE_THRESHOLD if trim_level > 1 else DEFAULT_SILENCE_THRESHOLD if trim_level == 0 else LAZY_SILENCE_THRESHOLD
    start_trim = detect_leading_silence(untrimmed_audio, silence_threshold=silence_threshold)
    end_trim = detect_leading_silence(untrimmed_audio.reverse(), silence_threshold=silence_threshold)
    duration = len(untrimmed_audio)
    trimmed_aud = untrimmed_audio[start_trim:duration - end_trim]
    return trimmed_aud


def convert_audio_recordings_list_into_an_mp3_file(data, exportfile:str, trim_level:int=0):
    """Convert a list of audio data into an MP3 file.

    Write the supplied list of data (probably MP3 to individual files.
    Use the pydub library to combine them into a single MP3. Save it
    to the specified pathname.

    Args:
        data: The list of MP3 data. I say 'list' because
            this is a *list* of several bytes, not several *bytes*. To
            access MP3 data #0, read data[0]. That's the first MP3 file.
            The second is data[1]. You get the picture, I hope.
        trim_level: If 0, don't trim. If 1, trim. If 2, trim aggressively.
        exportfile: The pathname of the output file.

    Returns:
        n/a

    Raises:
        Unknown.

    """
    suffix = 'mp3' if exportfile.endswith( 'mp3') else 'ogg'
    sounds = convert_audio_recordings_list_into_one_audio_recording(data=data, trim_level=trim_level, suffix=suffix)
    sounds.export(exportfile, format=suffix)
