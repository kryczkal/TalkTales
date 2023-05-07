from queue import SimpleQueue
from threading import Event

import pyaudio as pyaud


def produce_audio(stt_output: SimpleQueue, sr_output: SimpleQueue,
                  signal_events: dict[str, Event] = {}):
    """A function that produces audio packets in all ``outputs``

    This function should be a thread target
    and should not be called synchronously
    """

    freq = 48000
    # duration = 1000.0
    format = pyaud.paInt16
    chunk = 1200

    stream = pyaud.PyAudio().open(format=format, channels=1, rate=freq,
                                  input=True, frames_per_buffer=chunk)
    while True:
        set = bytes()
        for i in range(4):
            data = stream.read(chunk)
            stt_output.put(data)
            set += data
        sr_output.put(set)
