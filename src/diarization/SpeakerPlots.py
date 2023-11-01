import matplotlib.pyplot as plt
import numpy as np
from math import ceil, sqrt
import itertools
from .Speaker import Speaker

# Define the SpeakerPlots class
class SpeakerPlots:
    # Initialize the object with an ID, empty dictionary for plots, and number of speakers as 0
    def __init__(self, id: int) -> None:
        self.plots = {} # Holds all the plotting data points
        self.n_speakers = 0
        self.id = id
    # Method to add data points to a particular speaker's plot
    def add_to_plot(self, id, x, y) -> None:
        if id not in self.plots:
            self.plots[id] = []
            self.n_speakers +=1
        self.plots[id].append( (x, y) ) # Add the (x, y) point to the speaker's list of points

    # Method to create the plot using matplotlib
    def plot(self) -> None:
        n_rows = int(sqrt(self.n_speakers))
        n_cols = ceil(self.n_speakers / n_rows)

        # Loop through each speaker and create their subplot
        for plot_id in self.plots:
            plt.subplot(n_rows, n_cols, plot_id+1)
            plt.plot( [value[0] for value in self.plots[plot_id] ], [value[1] for value in self.plots[plot_id]] )
            plt.title(f"Speaker {plot_id}")

        # Uncomment the following lines if you want to manually set y-limit and figure size
        # plt.ylim = (5, 70)
        # plt.figure(figsize=(20,12))
        
        plt.suptitle(self.id)
        plt.tight_layout()
        plt.show()
        plt.close()
