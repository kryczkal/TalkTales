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
analyze_buffer = []
once = True
it = 200
#stop = 1
try:
    print("Recording audio... Press Ctrl+C to stop.")

    counter = 0
    analyze_counter = 0
    while True:
        Data = stream.read(Settings.CHUNK_SIZE)
        Temp = Sample(Data,
                      Vad.is_speech(Data, Settings.FREQUENCY),
                      counter * Settings.SEGMENT_DURATION_MS)

        counter += 1

        if once:
            mfcc_buffer = Temp.GetMfcc().T
            once = False
        if Temp.IsSpeech:
            analyze_buffer.append(Temp)
            mfcc_buffer = np.append(mfcc_buffer, Temp.GetMfcc().T, axis=0)

            analyze_counter += 1
            if analyze_counter % it != 0:
                continue

            speaker_gmm.train(mfcc_buffer)
            hypothetical_gmm.train(mfcc_buffer[-it:])

            divergence = gmm_kl(speaker_gmm.getModel(), hypothetical_gmm.getModel())
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
