from queue import Queue, SimpleQueue
from typing import Tuple
from threading import Event

from re import search


def voice_recognition(input: Queue, output: SimpleQueue,
                      signal_events: dict[str, Event] = {}
                      ) -> Tuple[int, float]:
    """A function that consumes audio packets from ``input``
    and produces timestamped speaker changes in ``output``

    This function should be a thread target
    and should not be called synchronously
    """

    speaker = 0

    # main loop
    while True:
        # get() waits until there's an item available by default
        packet = input.get()

        # debugging example
        if search(r'(?<=^<)\d(?=>)', packet[0]):
            speaker = (int)(search(r'(?<=<)\d(?=>)', packet[0]).group())

        ...  # processing

        output.put(speaker)
        input.task_done()
