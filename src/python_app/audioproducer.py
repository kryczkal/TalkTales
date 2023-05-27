from queue import SimpleQueue
from threading import Event
from settings import Settings

import pyaudio as pyaud


def produce_audio(stt_output: SimpleQueue, sr_output: SimpleQueue,
                  signal_events: dict[str, Event] = {}):
    """A function that produces audio packets in all ``outputs``

    This function should be a thread target
    and should not be called synchronously
    """

    freq = Settings.FREQUENCY
    # duration = 1000.0
    format = Settings.STREAMFORMAT
    chunk = Settings.CHUNK_SIZE

    stream = pyaud.PyAudio().open(format=format, channels=1, rate=freq,
                                  input=True, frames_per_buffer=chunk)

    while True:
        data = stream.read(chunk)
        stt_output.put(data)
        sr_output.put(data)
