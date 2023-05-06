import matplotlib.pyplot as plt
import numpy as np
from math import ceil, sqrt
import itertools
from Speaker import Speaker
class SpeakerPlots:
    def __init__(self) -> None:
        self.plots = {}
        self.n_speakers = 0

    def add_to_plot(self, id, x, y):
        if id not in self.plots:
            self.plots[id] = []
            self.n_speakers +=1
        self.plots[id].append( (x, y) )
    
    def plot(self):
        n_rows = int(sqrt(self.n_speakers))
        n_cols = ceil(self.n_speakers / n_rows)
        
        for plot_id in self.plots:
            plt.subplot(n_rows, n_cols, plot_id+1)
            plt.plot( [value[0] for value in self.plots[plot_id] ], [value[1] for value in self.plots[plot_id]] )
            plt.title(f"Speaker {plot_id}")
            
        # plt.ylim = (5, 70)
        # plt.figure(figsize=(20,12))
        
        plt.tight_layout()
        plt.show()
        plt.close()
