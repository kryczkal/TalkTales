from Sample import Sample
from librosa import display
import matplotlib as plt

def plot_mfcc(Sample):
    display.specshow()
    plt.title("Mel Coef")
    plt.show()