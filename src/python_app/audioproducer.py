from audioprocessing import audio_preprocessor
from queue import Queue
from typing import List

#import pyaudio # possible way to get an audio stream?

from random import randint

def produce_audio(outputs: List[Queue]):
    """A function that produces audio packets in all ``outputs``
    
    This function should be a thread target and should not be called synchronously
    """
    DEBUG_STRING = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.  <1>Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. <2>Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit <3>anim id est laborum.".split()
    j = 0
    print('audioproducer launched')
    while True:
        packet = None

        ... # get some audio packet

        # debugging example
        if randint(0, 1):
            if randint(0, 1):
                packet = (' ', j)
            elif j < len(DEBUG_STRING):
                packet = (DEBUG_STRING[j], j)
                j += 1

        if packet:
            processed_packet = audio_preprocessor(packet)
            for i in outputs:
                i.put(processed_packet)