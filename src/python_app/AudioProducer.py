from queue import SimpleQueue
from threading import Event
from ..Settings import Settings

import pyaudio as pyaud


def produce_audio(stt_output: SimpleQueue, sr_output: SimpleQueue,
                  signal_events: dict[str, Event] = {}):
    """A function that produces audio packets in all ``outputs``

    This function should be a thread target
    and should not be called synchronously
    """

    # duration = 1000.0
    stream = pyaud.PyAudio().open(format=Settings.STREAM_FORMAT,
                                  channels=Settings.CHANNELS,
                                  rate=Settings.FREQUENCY,
                                  frames_per_buffer=Settings.FRAMES_PER_SEGMENT,
                                  input=True,
                                  )

    while True:
        data = stream.read(Settings.FRAMES_PER_SEGMENT)
        stt_output.put(data)
        sr_output.put(data)
