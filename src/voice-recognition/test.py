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
from Gmm import Speaker, kl_distance
# from queue import Queue

audio = pyaudio.PyAudio()
stream = audio.open(format=Settings.STREAMFORMAT, channels=Settings.CHANNELS, rate=Settings.FREQUENCY, input=True, frames_per_buffer=Settings.CHUNK_SIZE)
Vad = webrtcvad.Vad(1)

speaker_gmm = Speaker()
hypothetical_gmm = Speaker()
analyze_buffer = []
once = True
it = 200
#stop = 1
try:
    print("Recording audio... Press Ctrl+C to stop.")

    counter = 0
    analyze_counter = 0
    while True:
        byte_data = stream.read(Settings.CHUNK_SIZE)
        Temp = VoiceSample(byte_data,
                      Vad.is_speech(byte_data, Settings.FREQUENCY),
                      counter * Settings.SEGMENT_DURATION_MS)

        counter += 1

        if once:
            mfcc_buffer = Temp.mfcc_get().T
            once = False

        if Temp.is_speech:
            analyze_buffer.append(Temp)
            #mfcc_buffer = np.vstack((mfcc_buffer, Temp.GetMfcc().T))
            #print("dodajemy:")
            #print(Temp.GetMfcc().T)
            mfcc_buffer = np.append(mfcc_buffer, Temp.mfcc_get().T, axis=0)
            #print("nowa konkatanacja")
            #print(mfcc_buffer)
            #if stop % 3 == 0:
            #    exit()
            #stop += 1
            analyze_counter += 1
            if analyze_counter % it != 0:
                continue

            speaker_gmm.model_train(mfcc_buffer)
            #print(mfcc_buffer.shape)
            #print("ostatnie", it)
            #print(mfcc_buffer[-it:].shape)
            hypothetical_gmm.model_train(mfcc_buffer[-it:])

            divergence = kl_distance(speaker_gmm.model_get(), hypothetical_gmm.model_get())
            print("KL divergence = ", divergence)

            #exit()


except KeyboardInterrupt:
    print("Recording stopped")

    analyze_buffer = CreateOverlappedData(analyze_buffer)
    ExtractInformation(analyze_buffer)

    for Num, Seg in enumerate(analyze_buffer):
        if Num < 5*7:
            plt.subplot(5,7,Num+1)
            plot_mfcc(Seg)

    plt.show()

finally:
    stream.stop_stream()
    stream.close()
    audio.terminate()
