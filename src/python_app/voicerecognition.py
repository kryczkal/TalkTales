from queue import Queue, SimpleQueue
from typing import Tuple

from re import search

def voice_recognition(input: Queue, output: SimpleQueue) -> Tuple[int, float]:
    """A function that consumes audio packets from ``input`` and produces timestamped speaker changes in ``output``
    
    This function should be a thread target and should not be called synchronously
    """
    
    speaker = 0

    # main loop
    while True:
        packet = input.get() # get() waits until there's an item available by default

        # debugging example
        if search('(?<=^<)\d(?=>)', packet[0]):
            speaker = (int)(search('(?<=<)\d(?=>)', packet[0]).group())
        
        ... # processing

        output.put(speaker)
        input.task_done()