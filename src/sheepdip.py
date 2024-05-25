'''
Created on May 24, 2024

@author: Tom Blackshaw
'''

from _queue import Empty
from array import array
from queue import Queue
from struct import pack
from sys import byteorder
from threading import Thread
import datetime
import os
import sys
import time
import wave

from speech_recognition.exceptions import UnknownValueError
import pyaudio

from my.classes.exceptions import StillAwaitingCachedValue
from my.classes.selfcachingcall import SelfCachingCall
from my.weather import WeatherSingleton as ws, generate_short_and_long_weather_forecast_messages

G_activation_codeword = 'hey Dad'
THRESHOLD = 500
NOOF_SILENCE = 32
CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
RATE = 44100

G_stop = False



def is_silent(snd_data):
    "Returns 'True' if below the 'silent' threshold"
    return max(snd_data) < THRESHOLD


def normalize(snd_data):
    "Average the volume out"
    MAXIMUM = 16384
    times = float(MAXIMUM) / max(abs(i) for i in snd_data)

    x = array('h')
    for i in snd_data:
        x.append(int(i * times))
    return x


def trim(snd_data):
    "Trim the blank spots at the start and end"

    def _trim(snd_data):
        snd_started = False
        x = array('h')

        for i in snd_data:
            if not snd_started and abs(i) > THRESHOLD:
                snd_started = True
                x.append(i)

            elif snd_started:
                x.append(i)
        return x

    # Trim to the left
    snd_data = _trim(snd_data)

    # Trim to the right
    snd_data.reverse()
    snd_data = _trim(snd_data)
    snd_data.reverse()
    return snd_data


def add_silence(snd_data, seconds):
    "Add silence to the start and end of 'snd_data' of length 'seconds' (float)"
    silence = [0] * int(seconds * RATE)
    x = array('h', silence)
    x.extend(snd_data)
    x.extend(silence)
    return x


def record():
    """
    Record a word or words from the microphone and
    return the data as an array of signed shorts.

    Normalizes the audio, trims silence from the
    start and end, and pads with 0.5 seconds of
    blank sound to make sure VLC et al can play
    it without getting chopped off.
    """
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=1, rate=RATE,
        input=True, output=True,
        frames_per_buffer=CHUNK_SIZE)

    num_silent = 0
    snd_started = False

    x = array('h')

    while 1:
        # little endian, signed short
        snd_data = array('h', stream.read(CHUNK_SIZE))
        if byteorder == 'big':
            snd_data.byteswap()
        x.extend(snd_data)

        silent = is_silent(snd_data)

        if silent and snd_started:
            num_silent += 1
        elif not silent and not snd_started:
            snd_started = True

        if snd_started and num_silent > NOOF_SILENCE:
            break

    sample_width = p.get_sample_size(FORMAT)
    stream.stop_stream()
    stream.close()
    p.terminate()

    x = normalize(x)
    x = trim(x)
    x = add_silence(x, 0.5)
    return sample_width, x


def speak_a_weather_report(tts, owner_name):
    shorter_msg, longer_msg = generate_short_and_long_weather_forecast_messages(ws.forecast, owner_name, testing=True)
    data = tts.audio(text=shorter_msg)
    del longer_msg
    tts.play(data)


def generate_weather_audio(tts, owner_name):
    shorter_msg, longer_msg = generate_short_and_long_weather_forecast_messages(ws.forecast, owner_name, testing=True)
    shorter_audio = tts.audio(text=shorter_msg)
    longer_audio = tts.audio(text=longer_msg)
    return {'shorter msg': shorter_msg, 'shorter audio':shorter_audio, 'longer msg': longer_msg, 'longer audio':longer_audio}


G_sorry_audio = None
G_fu2 = None
G_watch  = None
G_dowhatnow = None
G_our_cached_weather_report_messages = None
G_goodbye = None

def process_text(tts, text):
    global G_our_cached_weather_report_messages, G_stop
    print("voice =", tts.voice)
    if 'weather' in text:
        try:
            tts.play(G_our_cached_weather_report_messages.result['shorter audio'])
        except StillAwaitingCachedValue:
            tts.play(G_sorry_audio)
#        do_a_weather_report(tts, ws.forecast, tts.voice, 'Freya', True)c
    elif 'time' in text:
        tts.play(G_watch)
    elif 'screw you' in text:
        tts.play(G_fu2)
    elif 'bye' in text:
        tts.play(G_goodbye)
        G_stop = True
        sys.exit(0)
    else:
#        tts.say(text)
        tts.play(G_dowhatnow)


def record_to_file(path):
    "Records from the microphone and outputs the resulting data to 'path'"
    sample_width, data = record()
    data = pack('<' + ('h' * len(data)), *data)
    wf = wave.open(path, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(sample_width)
    wf.setframerate(RATE)
    wf.writeframes(data)
    wf.close()



def producer(queue, fname, r):
    import speech_recognition as sr
    while True:
        print("please speak a word into the microphone")
        try:
            sample_width, data = record()
            data = pack('<' + ('h' * len(data)), *data)
            queue.put((datetime.datetime.now(), sample_width, data))
            record_to_file(fname)
        except OSError:  # https://stackoverflow.com/questions/10733903/pyaudio-input-overflowed/
            print("Warning. Input overflowed. Losing a frame or two.")
        else:
            # os.system('mpv {fname}'.format(fname=fname))
            print("FORK ME! (FIXME) Trying to decode...")
            try:
                with sr.AudioFile(fname) as source:
                    # listen for the data (load audio to memory)
                    audio_data = r.record(source)
                    # recognize (convert from speech to text)
                    text = r.recognize_vosk(audio_data)
            except UnknownValueError:  # as e:
                time.sleep(.1)
                pass  # print("Failed to decode")
            else:
                queue.put((datetime.datetime.now(), text))  # print('result =', text)
        try:
            os.unlink(fname)
        except FileNotFoundError:
            pass  # print("Warning - {fname} not found. Cannot delete temp file.".format(fname=fname))


def consumer(queue, tts):
    print('Consumer: Running')
    new_timestamp = datetime.datetime.now()
    while True:
        sentence = ''
        # get a unit of work
        old_timestamp = new_timestamp
        new_timestamp, text = queue.get()
        if (new_timestamp - old_timestamp).microseconds >= 800999:
            sentence = sentence.strip()
            print("Sentence ==>", sentence)
            sentence = ''
        sentence += text + ' '
        print("BTW, text was", text, "and now sentence is", sentence)
#             tts.say(text)
        # check for stop
        if text is None:
            time.sleep(1)
        # report


def record_and_pack_from_next_audioin_burst():
    start_datestamp = datetime.datetime.now()
    sample_width, data = record()
    data = pack('<' + ('h' * len(data)), *data)
    finish_datestamp = datetime.datetime.now()
    return (start_datestamp, finish_datestamp, sample_width, data)


def indefinitely_record_and_pack_incoming_audio(audio_queue):
    global G_stop
    while not G_stop:
        try:
            data = record_and_pack_from_next_audioin_burst()
            audio_queue.put(data)
        except OSError as e:
            print("(indefinitely_record_and_pack_incoming_audio) Warning -- %s" % str(e))
            time.sleep(.1)


def convert_all_audio_in_queue(audio_queue, text_queue):
    import speech_recognition as sr
    r = sr.Recognizer()
    last_finish_ds = datetime.datetime.now()
    while True:
        try:
            start_datestamp, finish_datestamp, sample_width, data = audio_queue.get_nowait()
            interpause_in_microseconds = (last_finish_ds - start_datestamp).microseconds
            last_finish_ds = finish_datestamp
        except Empty:
            return
        else:
            audio_data = sr.AudioData(data, RATE, sample_width)
            text = r.recognize_vosk(audio_data)
            text_queue.put((start_datestamp, finish_datestamp, interpause_in_microseconds, text))

# def indefinitely_get_sentences(text_queue, sentences_queue):
#     global G_stop
#     sentence = ''
#     while True:
#         try:
#             start_ds, end_ds, pause_in_milliseconds, text = text_queue.get_nowait()
#         except Empty:
#             if G_stop:
#                 break
#             else:
# #                print('waiting...')
#                 time.sleep(1)
#         else:
#             print("text =", text)
#             sentence += text + ' '
#             if pause_in_milliseconds < SLOWTALKER_TIMEOUT_IN_MICROSECONDS:
# #                print("Waiting for more text")
#                 time.sleep(.1)
#             else:
#                 print("text =", text)
#                 sentence = sentence.strip()
#                 sentences_queue.put(sentence)
#                 print("==>", sentence, "<==")
#                 sentence = ''


def indefinitely_convert_all_audio(audio_queue, text_queue):
    global G_stop
    while not G_stop:
        convert_all_audio_in_queue(audio_queue, text_queue)

'''

sentence = ''
last_datestamp = datetime.datetime.now()
while True:
    try:
        start_ds, end_ds, pause_in_milliseconds, t = text_queue.get_nowait()
        text = eval(t)['text']
        print("text=", text)
        if (datetime.datetime.now()-last_datestamp).total_seconds() >= SLOWTALKER_TIMEOUT:
            sentence = sentence.strip()
            print("==>", sentence, "<==")
#             sentences_queue.put(sentence)
            sentence = ''
            last_datestamp = end_ds
    except Empty:
        time.sleep(.1)
    else:
        sentence += text + ' '

'''
def main():
    import vosk
    vosk.SetLogLevel(-1)
    import speech_recognition as sr
    global G_stop
    from my.classes.text2speechclass import Text2SpeechSingleton as tts
    global G_sorry_audio, G_fu2, G_watch, G_dowhatnow, G_our_cached_weather_report_messages, G_goodbye
#     process_text(tts, "What's the weather like?")
    r = sr.Recognizer()
    tts.voice = "Freya"
    owner_name = 'Chuckles'
    G_sorry_audio = tts.audio("Sorry, I'm still waiting for the weather forecast. Please try again later.")
    G_fu2 = tts.audio("Screw you too, {owner_name}! I'm over here, working my ass off, and you know what, you're not even worth it.".format(owner_name=owner_name))
    G_watch = tts.audio("It's time you got a watch, {owner_name}. Borrow some money from your Dad and buy one.".format(owner_name=owner_name))
    G_dowhatnow = tts.audio("I'm sorry. I don't understand.")
    G_goodbye = tts.audio("Toodles! Word to your mother's hair stylist, homie G!")
    G_our_cached_weather_report_messages = SelfCachingCall(180, generate_weather_audio, tts, owner_name)
    G_stop = False
    audio_queue = Queue()
    text_queue = Queue()
#    sentences_queue = Queue(maxsize=50)
    audio_thread = Thread(target=indefinitely_record_and_pack_incoming_audio, args=(audio_queue,))
    audio_thread.start()
    convertsounds_thread = Thread(target=indefinitely_convert_all_audio, args=(audio_queue, text_queue,))
    convertsounds_thread.start()
    # sentences_thread = Thread(target=indefinitely_get_sentences, args=(text_queue, sentences_queue,))
    # sentences_thread.start()
    print("Press Ctrl-C to quit.")
    sentence = ' '
    while True:
        if G_stop:
            break
        time.sleep(.2)
        if len(sentence) > 200:
            sentence = sentence[-200:]
        while True:
            try:
                _start_ds, _end_ds, _pause_in_milliseconds, text = text_queue.get_nowait()
                if ' : ' in text and '{' in text:
                    text = eval(text)['text'].strip()
                    sentence += text + ' '
                    print("Sentence :", sentence)
            except Empty:
                break
        findme = ' %s ' % (G_activation_codeword.strip()).lower()
        cutoff_point = sentence.lower().find(findme)
#         print("Can I find %s in %s? ==> %d" % (findme, sentence, cutoff_point))
        if cutoff_point >= 0:
            sentence = sentence[cutoff_point + len(findme):]
            print("Sentence :", sentence)
            process_text(tts, sentence)
            sentence = ' '
            # empty the text and audio buffers
            while True:
                try:
                    data = audio_queue.get_nowait()
                except Empty:
                    break
            while True:
                try:
                    data = text_queue.get_nowait()
                except Empty:
                    break
    G_stop = True
    audio_thread.join()
    convertsounds_thread.join()
#    sentences_thread.join()


if __name__ == '__main__':
    main()

