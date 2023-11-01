from queue import SimpleQueue
from threading import Event
from ..diarization.Diarizer import Diarizer


def speaker_detector(input_queue: SimpleQueue, output_queue: SimpleQueue,
                     signals: dict[Event]):
    # Random Diarizers
    recognizer = Diarizer(30)

    # print("Recording audio... Press Ctrl+C to stop.")
    # byte_counter = 0
    signals['ready'].set()
    while True:
        # print('speaker recognizer')
        byte_data = input_queue.get()

        if recognizer.diarize(byte_data):
            output_queue.put(True)

            # output.put(None)
