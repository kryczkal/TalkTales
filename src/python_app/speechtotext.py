from queue import Queue, SimpleQueue

def stt(input: Queue, output: SimpleQueue):
    while True:
        input.get() # get() waits until there's an item available by default
        word = ''
        timestamp = 0.0


        ... # processing

        if word:
            output.put((word, timestamp))
        input.task_done()
        
