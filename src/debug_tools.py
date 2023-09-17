from time import time

class Timer:
    def __init__(self) -> None:
        self.start()

    def __del__(self) -> None:
        self.stop()

    def start(self) -> float:
        self.start = time()
        return self.start

    def stop(self) -> float:
        stop = time()
        spent_time = stop - self.start

        print("Spent time:\nIn seconds: " + str(spent_time) 
              + "\nIn miliseconds: " + str(spent_time * 1e+3) 
              + "\nIn nanoseconds: " + str(spent_time * 1e+6) + '\n')

        return spent_time