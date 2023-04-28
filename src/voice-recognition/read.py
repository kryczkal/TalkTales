import pyaudio
import numpy as np
import time as t
import webrtcvad

from Sample import Sample
from VoiceRecog import *
from Settings import Settings

from plots import plot_mfcc
import matplotlib.pyplot as plt

audio = pyaudio.PyAudio()
stream = audio.open(format=Settings.STREAMFORMAT, channels=Settings.CHANNELS, rate=Settings.FREQUENCY, input=True, frames_per_buffer=Settings.CHUNK_SIZE)
Vad = webrtcvad.Vad(1)

try:
    print("Recording audio... Press Ctrl+C to stop.")
    AudioBuffer = []
    AnalyzeBuffer = []
    Counter = 0
    
    while True:
        Data = stream.read(Settings.CHUNK_SIZE)
        Temp = Sample(Data,
                        Vad.is_speech(Data, Settings.FREQUENCY), 
                        Counter * Settings.SEGMENT_DURATION_MS)
        
        Counter += 1

        AudioBuffer.append(Temp)

        if Temp.IsSpeech:
            AnalyzeBuffer.append(Temp)


except KeyboardInterrupt:
    print("Recording stopped")

    AnalyzeBuffer = CreateOverlappedData(AnalyzeBuffer)
    ExtractInformation(AnalyzeBuffer)

    for Num, Seg in enumerate(AnalyzeBuffer):
        if Num < 5*7:
            plt.subplot(5,7,Num+1)
            plot_mfcc(Seg)

    plt.show()

finally:
    stream.stop_stream()
    stream.close()
    audio.terminate()
