import pyaudio
import numpy as np
import time as t
from webrtcvad import Vad
from Sample import Sample
from Settings import Settings

from plots import plot_mfcc
import matplotlib.pylab

audio = pyaudio.PyAudio()
stream = audio.open(format=Settings.FORMAT, channels=Settings.CHANNELS,
                    rate=Settings.FREQUENCY, input=True, frames_per_buffer=Settings.CHUNK_SIZE)

try:
    print("Recording audio... Press Ctrl+C to stop.")
    buffer = []

    for i in range(100):
        buff = stream.read(Settings.CHUNK_SIZE)
        frame = np.frombuffer(buff, dtype=np.float32)
        frame = frame.astype(np.float32, order='C') / 32768.0 #żeby dzialalo z settings dla vad

        sample = Sample(frame)
        sample.get_mfcc()
        buffer.append(sample)
    for i in range(100):
        matplotlib.pylab.subplot(10, 10, i + 1)
        plot_mfcc(buffer[i])

    matplotlib.pylab.show()

except KeyboardInterrupt:
    print("Recording stopped")
finally:
    stream.stop_stream()
    stream.close()
    audio.terminate()
