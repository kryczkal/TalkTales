import time

import pyaudio
import numpy as np
import time as t
import webrtcvad
import wave
import torch
import torchaudio

from Sample import VoiceSample
from Settings import Settings

from plots import plot_mfcc
import matplotlib.pyplot as plt
from Speaker import Speaker, kl_distance
from Recognizer import Recongnizer


audio = pyaudio.PyAudio()

torchaudio.set_audio_backend("soundfile")
torch.set_num_threads(1)
vad, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad',
                              model='silero_vad',
                              force_reload=True)
(get_speech_timestamps,
 save_audio,
 read_audio,
 VADIterator,
 collect_chunks) = utils

recognizer = Recongnizer(30)

READ_FROM_FILE = False

if READ_FROM_FILE:
    filename='src/voice_recognition/nagrywka2.wav'
    
    wav =  wave.open(filename, 'rb')

    format = audio.get_format_from_width(wav.getsampwidth())
    if  format != Settings.STREAMFORMAT: # expected stream format
        raise Exception(f"File is in wrong format: {format}")

    channels = wav.getnchannels()
    if channels != Settings.CHANNELS: # expected channel count
        raise Exception(f"File has more channels than expected: {channels}")
    
    rate = wav.getframerate()
    if rate != Settings.FREQUENCY: # expected rate
        raise Exception(f"File is in has wrong freq: {rate}")
 
else:   
    stream = audio.open(format=Settings.STREAMFORMAT, 
                        channels=Settings.CHANNELS, 
                        rate=Settings.FREQUENCY, 
                        input=True, 
                        frames_per_buffer=Settings.CHUNK_SIZE)

try:
    print("Recording audio... Press Ctrl+C to stop.")
    while(True):
        if READ_FROM_FILE:
            byte_data = wav.readframes(Settings.CHUNK_SIZE)
        else:
            byte_data = stream.read(Settings.CHUNK_SIZE)
            
        sample = VoiceSample(byte_data)
        sample.speech_probability =  vad(torch.from_numpy(sample.data_convert()), Settings.FREQUENCY).item()

        #print(f"speech probability: {sample.speech_probability}")

        if sample.speech_probability > 0.60: 
            recognizer.append_data(sample.mfcc_get().T)
            recognizer.train()
            if recognizer.check_for_speaker_change():
                print("speaker changed!")
            recognizer.adjust()
                
except KeyboardInterrupt:
    print("Stopped recording")