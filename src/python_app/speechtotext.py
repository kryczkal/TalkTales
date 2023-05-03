from queue import Queue, SimpleQueue
from typing import Tuple
from threading import Event

from re import sub


def stt(input: Queue, output: SimpleQueue,
        signal_events: dict[str, Event] = {}) -> Tuple[str, float]:
    """A function that consumes audio packets from ``input``
    and produces timestamped speaker words in ``output``

    This function should be a thread target
    and should not be called synchronously
    """
    while True:
        # get() waits until there's an item available by default
        packet = input.get()
        word = ''
        timestamp = 0.0  # noqa: F841

        # debugging example
        word = sub(r'<\d>', '', packet[0]).strip()

        ...  # processing

        output.put(word)
        input.task_done()
