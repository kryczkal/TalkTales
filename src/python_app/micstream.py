from speech_recognition import AudioSource
from queue import SimpleQueue
from settings import Settings

import pyaudio as pa


class QueueStream(object):
    """Instead of a file, its read is a blocking get call to a queue."""
    # hehe.
    def __init__(self, queue: SimpleQueue) -> None:
        self.queue = queue

    def read(self, *args) -> bytes:
        return self.queue.get()


class RemoteStreamSource(AudioSource):
    def __init__(self, queue: SimpleQueue, sample_rate=Settings.FREQUENCY,
                 chunk_size=Settings.CHUNK_SIZE // 4):
        self.stream = QueueStream(queue)
        self.SAMPLE_RATE = sample_rate
        self.format = Settings.STREAMFORMAT
        self.SAMPLE_WIDTH = pa.get_sample_size(self.format)
        self.CHUNK = chunk_size

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass
