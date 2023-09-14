time_start = 0
import pyaudio
import numpy as np
import time as t
import torch
import torchaudio
import os
from tqdm import tqdm

from Sample import VoiceSample
from Settings import Settings

import matplotlib.pyplot as plt
from Speaker import Speaker, kl_distance
from Recognizer import Recongnizer
import itertools
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

rn = np.random.RandomState(26)

# Random Recongnizers
recognizers = [Recongnizer(30,1)]

READ_FROM_FILE = True

if READ_FROM_FILE:
    filename='src/diarization/nag2.wav'
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
    timestamp_error = 0
    if READ_FROM_FILE:
        with tqdm(total=num_chunks) as pbar:
            while(byte_data):
                byte_data=wav_data[byte_counter*4*Settings.FRAMES_PER_SEGMENT:(byte_counter+1)*4*Settings.FRAMES_PER_SEGMENT]
                byte_counter += 1
                if len(byte_data) < 4*Settings.FRAMES_PER_SEGMENT:
                    byte_data = False
                    break
                pbar.update(1)

                sample = VoiceSample(byte_data)
                try:
                    sample.speech_probability =  vad(torch.from_numpy(sample.data_convert()), Settings.FREQUENCY).item()
                except ValueError:
                    sample.speech_probability = 0.0
                    print(ValueError)

                #if sample.speech_probability <= 0.60:
                #    print(f"speech probability: {sample.speech_probability}")
                if sample.speech_probability > 0.60: 
                    for recognizer in recognizers:
                        recognizer.append_data(sample.mfcc_get().T, timestamp_error)
                        timestamp_error = 0
                        recognizer.train()
                        recognizer.check_for_speaker_change()
                        recognizer.adjust()
                else:
                    timestamp_error += Settings.SEGMENT_DURATION_MS / 1000
    else:
        while(True):
            byte_data = stream.read(Settings.FRAMES_PER_SEGMENT)

            sample = VoiceSample(byte_data)
            sample.speech_probability =  vad(torch.from_numpy(sample.data_convert()), Settings.FREQUENCY).item()

            #if sample.speech_probability <= 0.60:
            #    print(f"speech probability: {sample.speech_probability}")
            if sample.speech_probability > 0.60: 
                for recognizer in recognizers:
                    recognizer.append_data(sample.mfcc_get().T, timestamp_error)
                    timestamp_error = 0
                    recognizer.train()
                    recognizer.check_for_speaker_change()
                    recognizer.adjust()
            else:
                timestamp_error += Settings.SEGMENT_DURATION_MS / 1000
                
except KeyboardInterrupt:
    print("Stopped recording")
except IndexError:
    print("IndexError")
except ValueError:
    print("ValueError - end of file")
finally:
    pass

if Settings.MAKE_PLOTS:
    for recognizer in recognizers:
        recognizer.plot()
