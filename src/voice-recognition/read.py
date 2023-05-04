import time

import pyaudio
import numpy as np
import time as t
import webrtcvad
import wave

from Sample import VoiceSample
from VoiceRecog import *
from Settings import Settings

from plots import plot_mfcc
import matplotlib.pyplot as plt
from Speaker import Speaker, kl_distance
from Recognizer import Recognizer

audio = pyaudio.PyAudio()
Vad = webrtcvad.Vad(1)

READ_FROM_FILE = True

if READ_FROM_FILE:
    filename='src/voice-recognition/nagrywka1.wav'
    
    wav =  wave.open(filename, 'rb')

    format = audio.get_format_from_width(wav.getsampwidth())
    if  format != Settings.STREAMFORMAT:
        raise Exception(f"File is in wrong format: {format}")

    channels = wav.getnchannels()
    if channels != Settings.CHANNELS:
        raise Exception(f"File has more channels than expected: {channels}")
    rate = wav.getframerate()
    if rate != Settings.FREQUENCY:
        raise Exception(f"File is in has wrong freq: {rate}")
 
else:   
    stream = audio.open(format=Settings.STREAMFORMAT, channels=Settings.CHANNELS, rate=Settings.FREQUENCY, input=True, frames_per_buffer=Settings.CHUNK_SIZE)


Recognizer = Recognizer()

once = True
it = 300
analyze_counter = 0

all_divergances = []
divergances = []
speaker_change_timestamps = []
max_id = 1

try:
    print("Recording audio... Press Ctrl+C to stop.")

    counter = 0

    while True:
        
        if READ_FROM_FILE:
            byte_data = wav.readframes(Settings.CHUNK_SIZE)
        else:
            byte_data = stream.read(Settings.CHUNK_SIZE)
            
        sample = VoiceSample(byte_data,
                            Vad.is_speech(byte_data, Settings.FREQUENCY),
                            counter * Settings.SEGMENT_DURATION_MS)
        counter += 1

        if once:
            mfcc_buffer = sample.mfcc_get().T
            once = False
            
        if sample.is_speech:
            mfcc_buffer = np.append(mfcc_buffer, sample.mfcc_get().T, axis=0)

            analyze_counter += 1
            if analyze_counter % it != 0:
                continue

            Recognizer.hypothetical_speaker.model_train(mfcc_buffer[-it:])
            Recognizer.current_speaker.model_train(mfcc_buffer)
            divergence, did_change = Recognizer.compare()
            print("KL divergence = ", divergence)
            Recognizer.divergances.append(divergence)
            all_divergances.append(divergence)

            if analyze_counter < 2*it:
                continue
            
            if did_change:
                print("Speaker changed!!")
                speaker_change_timestamps.append(np.floor(counter/300))
                max_id+=1
                once = True
                analyze_counter = 0
                Recognizer.current_speaker.model_train(mfcc_buffer[-it:])

            
            #exit()
except KeyboardInterrupt:
    print("Keyboard Interrupt")

finally:
    print("Recording stopped")
    domain = np.linspace(1, len(all_divergances), len(all_divergances))
    domain *= it / 100
    
    plt.plot(domain, all_divergances)
    plt.plot(speaker_change_timestamps, np.ones((1,len(speaker_change_timestamps)))*100, marker='x')
    
    plt.show()
    stream.stop_stream()
    stream.close()
    audio.terminate()