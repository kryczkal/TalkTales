from queue import Queue, SimpleQueue
from typing import Tuple

from re import sub

def stt(input: Queue, output: SimpleQueue) -> Tuple[str, float]:
    """A function that consumes audio packets from ``input`` and produces timestamped speaker words in ``output``
    
    This function should be a thread target and should not be called synchronously
    """
    print('thread stt launched')

    while True:
        packet = input.get() # get() waits until there's an item available by default
        word = ''
        timestamp = 0.0

        word = sub('<\d>', '', packet[0]).strip()
        
        ... # processing

        output.put(word)
        input.task_done()
        
