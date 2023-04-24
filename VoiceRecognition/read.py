import pyaudio
import numpy as np
import time as t
from webrtcvad import Vad

from Sample import Sample
from settings import Settings

from plots import plot_mfcc

audio = pyaudio.PyAudio()
stream = audio.open(format=Settings.FORMAT, channels=Settings.CHANNELS, rate=Settings.FREQUENCY, input=True, frames_per_buffer=Settings.CHUNK_SIZE)

try:
    print("Recording audio... Press Ctrl+C to stop.")
    buffer = []
    while True:
        t.sleep(1)
        y = np.frombuffer(stream.read(Settings.CHUNK_SIZE),np.dtype(int))
        if(Vad.is_speech(y)): continue
        data = Sample(y)
        data.get_mfccs()
        plot_mfcc(data)

except KeyboardInterrupt:
    print("Printing stopped")
finally:
    stream.stop_stream()
    stream.close()
    audio.terminate()