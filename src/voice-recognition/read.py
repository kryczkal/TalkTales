import time

import pyaudio
import numpy as np
import time as t
import webrtcvad

from Sample import VoiceSample
from VoiceRecog import *
from Settings import Settings

from plots import plot_mfcc
import matplotlib.pyplot as plt
from Speaker import Speaker, kl_distance
from Recognizer import Recognizer

audio = pyaudio.PyAudio()
stream = audio.open(format=Settings.STREAMFORMAT, channels=Settings.CHANNELS, rate=Settings.FREQUENCY, input=True, frames_per_buffer=Settings.CHUNK_SIZE)
Vad = webrtcvad.Vad(1)

Recognizer = Recognizer()

once = True
it = 300
analyze_counter = 0

all_divergances = []
divergances = []
max_id = 1

try:
    print("Recording audio... Press Ctrl+C to stop.")

    counter = 0

    while True:
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

            Recognizer.current_speaker.model_train(mfcc_buffer)
            Recognizer.hypothetical_speaker.model_train(mfcc_buffer[-it:])
            divergence, did_change = Recognizer.compare()
            print("KL divergence = ", divergence)
            Recognizer.divergances.append(divergence)
            all_divergances.append(divergence)

            if analyze_counter < 3*it:
                continue

            
            if did_change:
                print("Speaker changed!!")
                max_id+=1
                once = False
                analyze_counter = 0
            Recognizer.current_speaker.model_train(mfcc_buffer)
            
            #exit()
except KeyboardInterrupt:
    print("Recording stopped")
    plt.plot(all_divergances)
    plt.show()

finally:
    stream.stop_stream()
    stream.close()
    audio.terminate()
