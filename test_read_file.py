time_start = 0
import pyaudio
import numpy as np
import time as t
import os
from tqdm import tqdm

from src.diarization.Sample import VoiceSample
from src.Settings import Settings

import matplotlib.pyplot as plt
from src.diarization.Speaker import Speaker, kl_distance
from src.diarization.Diarizer import Diarizer
import itertools
audio = pyaudio.PyAudio()

diarizer = Diarizer()

READ_FROM_FILE = False

if READ_FROM_FILE:
    filename='assets/nag2.wav'
    filesize = os.path.getsize(filename)
 
    with open(filename, 'rb') as wav:
        header = wav.read(100)
        byte_data = True
        num_chunks = filesize // Settings.FRAMES_PER_SEGMENT / 4
        wav_data = wav.read()

else:   
    stream = audio.open(format=Settings.STREAM_FORMAT, 
                        channels=Settings.CHANNELS, 
                        rate=Settings.FREQUENCY, 
                        input=True, 
                        frames_per_buffer=Settings.FRAMES_PER_SEGMENT)

try:
    print("Recording audio... Press Ctrl+C to stop.")
    byte_counter = 0
    silent_seconds = 0
    if READ_FROM_FILE:
        with tqdm(total = num_chunks) as pbar:
            while(byte_data):
                byte_data = wav_data[byte_counter*4*Settings.FRAMES_PER_SEGMENT:(byte_counter+1)*4*Settings.FRAMES_PER_SEGMENT]
                byte_counter += 1
                if len(byte_data) < 4*Settings.FRAMES_PER_SEGMENT:
                    byte_data = False
                    break
                pbar.update(1)

                diarizer.diarize(byte_data)
    else:
        while(True):
            byte_data = stream.read(Settings.FRAMES_PER_SEGMENT)
            diarizer.diarize(byte_data)
                
except KeyboardInterrupt:
    print("Stopped recording")
except IndexError:
    print("IndexError")
except ValueError:
    print("ValueError - end of file")
finally:
    pass

if Settings.MAKE_PLOTS:
    diarizer.plot()
