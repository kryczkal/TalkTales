from Sample import Sample
from librosa import display
import matplotlib.pyplot as plt

def plot_mfcc(Sample):
    im = display.specshow(Sample.mfcc)
    # plt.colorbar(im)
    plt.title("Mel Coef")
    # plt.show()
