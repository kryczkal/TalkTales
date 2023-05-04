import time

import pyaudio
import numpy as np
import time as t
import webrtcvad

from Sample import Sample
from VoiceRecog import *
from Settings import Settings

from plots import plot_mfcc
import matplotlib.pyplot as plt
from Gmm import Gmm, gmm_kl

audio = pyaudio.PyAudio()
stream = audio.open(format=Settings.STREAMFORMAT, channels=Settings.CHANNELS, rate=Settings.FREQUENCY, input=True, frames_per_buffer=Settings.CHUNK_SIZE)
Vad = webrtcvad.Vad(1)

speaker_gmm = Gmm()
hypothetical_gmm = Gmm()
hypothetical_gmm2 = Gmm()
analyze_buffer = []
once = True
it = 300
divergances = []
divergances2 = []
#stop = 1
try:
    print("Recording audio... Press Ctrl+C to stop.")

    counter = 0
    analyze_counter = 1

    while True:
        Data = stream.read(Settings.CHUNK_SIZE)
        Temp = Sample(Data,
                      Vad.is_speech(Data, Settings.FREQUENCY),
                      counter * Settings.SEGMENT_DURATION_MS)

        counter += 1

        if once:
            mfcc_buffer = Temp.GetMfcc().T
            once = False

        if counter < 600 and Temp.IsSpeech:
            np.append(mfcc_buffer, Temp.GetMfcc().T, axis=0)   
            continue         
            
        if Temp.IsSpeech:
            analyze_buffer.append(Temp)
            mfcc_buffer = np.append(mfcc_buffer, Temp.GetMfcc().T, axis=0)

            analyze_counter += 1
            if analyze_counter % it != 0:
                continue

            speaker_gmm.train(mfcc_buffer)
            hypothetical_gmm.train(mfcc_buffer[-it:])
            hypothetical_gmm2.train(mfcc_buffer[-it*2:-it])

            divergence = gmm_kl(speaker_gmm.getModel(), hypothetical_gmm.getModel())
            divergence2 = gmm_kl(hypothetical_gmm2.getModel(), hypothetical_gmm.getModel())
            print("KL divergence = ", divergence)
            divergances.append(divergence)
            divergances2.append(divergance2)
            #exit()


except KeyboardInterrupt:
    print("Recording stopped")
    plt.plot(divergances)
    plt.plot(divergances2)
    plt.show()

finally:
    stream.stop_stream()
    stream.close()
    audio.terminate()
