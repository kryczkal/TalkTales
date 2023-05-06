import matplotlib.pyplot as plt
import numpy as np
from math import ceil, sqrt

from Speaker import Speaker
class SpeakerPlots:
    def __init__(self) -> None:
        self.plots = []
        self.n_speakers = 0

    def add_plot(self, id, speaker_data):
        self.n_speakers +=1
        self.plots.append( (id, speaker_data) )
    
    def plot(self):
        n_rows = int(sqrt(self.n_speakers))
        n_cols = ceil(self.n_speakers / n_rows)

        fig, axs = plt.subplots(n_rows, n_cols, figsize=(10, 10))
        for i in range(self.n_speakers):
            row = i // n_cols
            col = i % n_cols
            ax = axs[row, col]
            ax.plot([0, 1], [0, 1])
            ax.set_title(f"Speaker {i+1}"
        fig.tight_layout()
        plt.show()