from queue import SimpleQueue
from threading import Event
from ..diarization.Diarizer import Diarizer

def speaker_detector(input: SimpleQueue, output: SimpleQueue,
                     signals: dict[Event]):

    # Random Recongnizers
    recognizer = Diarizer(30, 0)

    # print("Recording audio... Press Ctrl+C to stop.")
    # byte_counter = 0
    signals['ready'].set()
    while True:
        # print('speaker recognizer')
        byte_data = input.get()

        if recognizer.diarize(byte_data):
            output.put(True)

            # output.put(None)
