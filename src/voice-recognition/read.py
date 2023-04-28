import pyaudio
import numpy as np
import time as t
import webrtcvad
import matplotlib.pyplot as plt

from Sample import Sample
from VoiceRecog import *
from Settings import Settings

from Debug.plots import *
from Debug.tablice import *


DebugCalosci = False
DebugOkienek = False
DebugOkienko = False
DebugSingleMfcc = False
DebugAnalyzeMfcc = True

audio = pyaudio.PyAudio()
stream = audio.open(format=Settings.STREAMFORMAT, channels=Settings.CHANNELS, rate=Settings.FREQUENCY, input=True, frames_per_buffer=Settings.CHUNK_SIZE)
Vad = webrtcvad.Vad(3)

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
    print("Recording Stopped")

    if DebugAnalyzeMfcc:
        MfccPlot = SetupConcatenatedMfccArray(AnalyzeBuffer)
        PlotMfccFromArray(MfccPlot)
        plt.show()

    if DebugSingleMfcc:
        AnalyzeBuffer = CreateOverlappedData(AnalyzeBuffer)
        ExtractInformation(AnalyzeBuffer)  

        PlotMfcc(AnalyzeBuffer[0])
        plt.show()

    if DebugCalosci:
        WholeAudio = CatList(AudioBuffer)
        SetupWholeAudioComponents(WholeAudio)
        PlotMel(WholeAudio)
        plt.show()

        plt.close()
        PartedAudio = CatList(AnalyzeBuffer)
        SetupWholeAudioComponents(PartedAudio)
        PlotMel(PartedAudio)
        plt.show()

        plt.close()



    if DebugOkienek:
        AnalyzeBuffer = CreateOverlappedData(AnalyzeBuffer)
        ExtractInformation(AnalyzeBuffer)  



        for Num, Seg in enumerate(AnalyzeBuffer):
            if Num < 9*16:
                plt.subplot(9,16,Num+1)
                PlotMfcc(Seg)

        plt.show()


    if DebugOkienko:
        AnalyzeBuffer = CreateOverlappedData(AnalyzeBuffer)
        ExtractInformation(AnalyzeBuffer)  

        plt.subplot(2,2,1)
        PlotMfcc(AnalyzeBuffer[20])
        plt.subplot(2,2,2)
        PlotMfcc(AnalyzeBuffer[40])
        plt.subplot(2,2,3)
        PlotMfcc(AnalyzeBuffer[60])
        plt.subplot(2,2,4)
        PlotMfcc(AnalyzeBuffer[80])

        plt.show()
        plt.close()

finally:
    stream.stop_stream()
    stream.close()
    audio.terminate()
