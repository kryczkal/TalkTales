import pyaudio
import numpy as np
import time as t
from webrtcvad import Vad
from Sample import Sample
from Settings import Settings

from plots import plot_mfcc
import matplotlib.pylab

audio = pyaudio.PyAudio()
stream = audio.open(format=Settings.STREAMFORMAT, channels=Settings.CHANNELS,
                    rate=Settings.FREQUENCY, input=True, frames_per_buffer=Settings.CHUNK_SIZE)

try:
    print("Recording audio... Press Ctrl+C to stop.")
    buffer = []
    not_detected = 0
    num_appended = 0
    append = True
    for i in range(0, 200):
        buff = stream.read(Settings.CHUNK_SIZE)
        frame = np.frombuffer(buff, dtype=np.int16)
        frame = frame.astype(np.float32, order='C') / 32768.0
        vad = Vad()

        if not vad.is_speech(buf=buff, sample_rate=Settings.FREQUENCY):
            not_detected += 1
            continue
        sample = Sample(frame)

        if append:
            buffer.append(sample)
            append = False
        else:
            buffer[num_appended].concatenate_data(sample)
            buffer[num_appended].get_mfcc()
            append = True
            num_appended += 1
    print("frames with no voice: ", not_detected)
    for i in range(0, len(buffer)):
        matplotlib.pylab.subplot(10, 10, i+1)

        plot_mfcc(buffer[i])

    matplotlib.pylab.show()

except KeyboardInterrupt:
    print("Recording stopped")
finally:
    stream.stop_stream()
    stream.close()
    audio.terminate()
