import time

import pyaudio
import numpy as np
import time as t
import webrtcvad
import wave

from Sample import VoiceSample
from Settings import Settings

from plots import plot_mfcc
import matplotlib.pyplot as plt
from Speaker import Speaker, kl_distance
from Recognizer import Recongnizer

# The code imports necessary libraries and files such as pyaudio, webrtcvad, numpy, Sample, VoiceRecog, Settings, plots, Speaker, and Recognizer. 
# # The code sets a boolean variable 'READ_FROM_FILE' to True, which determines whether the audio is being read from a file or recorded live.
# If READ_FROM_FILE is True, the code reads an audio file, checks if the file is in the expected format, channels, and frequency and sets those 
# values to their expected ones.
# If READ_FROM_FILE is False, the code initializes pyaudio, sets the stream settings using the Settings class, and opens the audio stream.
# The code has a try and except block which records the audio and divides it into small frames. It then passes these frames to voice_recognition 
# to identify individual speakers and measure their Kullig-Leiber (KL) divergence between their speech feature vectors. 
# It records these values and also takes into account if the speaker changes during the call. If a change in speaker is detected, then the code 
# knows that a new speaker has been detected and stores the time and the values of KL divergence. 
# Finally, it plots a graph showcasing the changes in speaker KL divergence over time. After runtime, this plot showcases the speaker changes 
# during the conversation.
# When the recording has finished, the pyaudio stream is stopped and closed.



audio = pyaudio.PyAudio()
vad = webrtcvad.Vad(1)

READ_FROM_FILE = False

if READ_FROM_FILE:
    filename='src/voice-recognition/nagrywka1.wav'
    
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


recognizer = Recongnizer()

once = True
it = 300
analyze_counter = 0

all_divergences = []
divergences = []
speaker_change_timestamps = []
max_id = 1

try:
    print("Recording audio... Press Ctrl+C to stop.")
    data_counter = 0

    while True:
        
        if READ_FROM_FILE:
            byte_data = wav.readframes(Settings.CHUNK_SIZE)
        else:
            byte_data = stream.read(Settings.CHUNK_SIZE)
            
        sample = VoiceSample(byte_data,
                            vad.is_speech(byte_data, Settings.FREQUENCY),
                            data_counter * Settings.SEGMENT_DURATION_MS)
        
        if once:
            mfcc_buffer = sample.mfcc_get().T
            once = False
            
        if sample.speech_probability:
            mfcc_buffer = np.append(mfcc_buffer, sample.mfcc_get().T, axis=0)

            analyze_counter += 1
            data_counter += 1

            if analyze_counter % it != 0:
                continue

            recognizer.hypothetical_speaker.model_train(mfcc_buffer[-it:])
            recognizer.current_speaker.model_train(mfcc_buffer)

            divergence, did_change = recognizer.check_for_speaker_change()
            recognizer.divergences.append(divergence)
            all_divergences.append(divergence)
            print("KL divergence = ", divergence)
            
            if analyze_counter < 2*it:
                continue
            
            if did_change:
                print("Speaker changed!!")

                speaker_change_timestamps.append( (np.floor(data_counter/100), divergence) )
                recognizer.current_speaker.model_train(mfcc_buffer[-it:])
                max_id+=1
                mfcc_buffer = sample.mfcc_get().T
                analyze_counter = 0
                
            
            #exit()
except KeyboardInterrupt:
    print("Keyboard Interrupt")

finally:
    print("Recording stopped")
    domain = np.linspace(1, len(all_divergences), len(all_divergences))
    domain *= it / 100
    
    plt.plot(domain, all_divergences)
    plt.scatter( [stamp[0] for stamp in speaker_change_timestamps], [stamp[1] for stamp in speaker_change_timestamps], marker = 'x', color='r')
    # i want a plot that is displayed on top of another plot, and has a big 'X' mark of red color
    plt.show()
    if not READ_FROM_FILE:
        stream.stop_stream()
        stream.close()
    audio.terminate()