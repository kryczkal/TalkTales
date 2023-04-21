from audiopreprocessor import audio_processing
from queue import Queue
from typing import List

def produce(outputs: List[Queue]):
    while True:
        packet = None

        ... # get some audio packet or sth
        if packet:
            processed_packet = audio_processing(packet)
            for i in outputs:
                i.put(processed_packet)