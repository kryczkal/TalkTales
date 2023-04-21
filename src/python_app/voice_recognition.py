from queue import Queue, SimpleQueue

def voicerecognition(input: Queue, output: SimpleQueue):
    # start with first speaker
    lastspeaker = 0

    # main loop
    while True:
        input.get() # get() waits until there's an item available by default
        speaker = 0
        timestamp = 0.0

        ... # processing

        if speaker != lastspeaker:
            lastspeaker = speaker
            output.put((speaker, timestamp))
        input.task_done()