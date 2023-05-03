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
from GMM import GMM

audio = pyaudio.PyAudio()
stream = audio.open(format=Settings.STREAMFORMAT, channels=Settings.CHANNELS, rate=Settings.FREQUENCY, input=True, frames_per_buffer=Settings.CHUNK_SIZE)
Vad = webrtcvad.Vad(1)

audio_buffer = []
analyze_buffer = []

gmm_buffer = np.zeros((13, 1))
Gmm = GMM(np.array(gmm_buffer))

try:
    print("Recording audio... Press Ctrl+C to stop.")

    counter = 0

    while True:
        Data = stream.read(Settings.CHUNK_SIZE)
        Temp = Sample(Data,
                      Vad.is_speech(Data, Settings.FREQUENCY),
                      counter * Settings.SEGMENT_DURATION_MS)
        
        counter += 1


        audio_buffer.append(Temp)

        if Temp.IsSpeech:
            analyze_buffer.append(Temp)
            gmm_buffer = np.concatenate((gmm_buffer, Temp.GetMfcc()), axis=1)

            start_time = time.time()
            model = GMM(np.array(gmm_buffer))
            end_time = time.time()
            print("zajelo to:", end_time-start_time)

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
