from vosk import Model, KaldiRecognizer
from queue import SimpleQueue
from threading import Event
from os.path import realpath
from json import loads
from ..Settings import Settings


def speech_to_text(input_queue: SimpleQueue, output_queue: SimpleQueue,
                   signals: dict[Event]):
    model_path = realpath('./vosk-model-small-pl-0.22')
    model = Model(model_path, lang='pl')
    recognizer = KaldiRecognizer(model, Settings.FREQUENCY)
    signals['ready'].set()
    time = 0
    while not signals['stop'].is_set():
        data = input_queue.get()

        time += 1
        if recognizer.AcceptWaveform(data):
            text = loads(recognizer.Result())['text']
            if text:
                output_queue.put((time, text))
