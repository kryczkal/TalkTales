time_start = 0
import pyaudio
import numpy as np
import time as t
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

READ_FROM_FILE = True

if READ_FROM_FILE:
    filename='src/voice_recognition/nag3.wav'
 
    with open(filename, 'rb') as wav:
        header = wav.read(100)
        wav_data = wav.read()

else:   
    stream = audio.open(format=Settings.STREAMFORMAT, 
                        channels=Settings.CHANNELS, 
                        rate=Settings.FREQUENCY, 
                        input=True, 
                        frames_per_buffer=Settings.CHUNK_SIZE)

try:
    print("Recording audio... Press Ctrl+C to stop.")
    wav_counter = 0
    timestamp_error = 0
    while(True):
        if READ_FROM_FILE:
            byte_data=wav_data[wav_counter*4*Settings.CHUNK_SIZE:(wav_counter+1)*4*Settings.CHUNK_SIZE]
            wav_counter+=1
        else:
            byte_data = stream.read(Settings.CHUNK_SIZE)

        sample = VoiceSample(byte_data)
        sample.speech_probability =  vad(torch.from_numpy(sample.data_convert()), Settings.FREQUENCY).item()

        #if sample.speech_probability <= 0.60:
        #    print(f"speech probability: {sample.speech_probability}")
        if sample.speech_probability > 0.60: 
            recognizer.append_data(sample.mfcc_get().T, timestamp_error)
            timestamp_error = 0
            recognizer.train()
            if recognizer.check_for_speaker_change():
                print("speaker changed!")
            recognizer.adjust()
        else:
            timestamp_error += Settings.SEGMENT_DURATION_MS / 1000

                
except KeyboardInterrupt:
    print("Stopped recording")
except IndexError:
    print("Lubudubu")
except ValueError:
    print("lololololo")
finally:
    if Settings.MAKE_PLOTS:
        recognizer.plot()