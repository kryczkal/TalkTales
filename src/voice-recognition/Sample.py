import numpy as np

from Settings import Settings
import librosa
import librosa.feature
import numpy


class Sample:
    def __init__(self, data: np.ndarray):
        self.data = data
        self.mfcc = 0
        self.mel = 0

    def get_mfcc(self):
        self.mel = librosa.feature.melspectrogram(y=self.data, sr=Settings.FREQUENCY)
        self.mfcc = librosa.feature.mfcc(y=self.data, S=self.mel, sr=Settings.FREQUENCY, n_mfcc=13, fmin=100, fmax=8000, lifter=1)

    def concatenate_data(self, s):
        self.data = numpy.concatenate((self.data, s.data), axis=None)
        return self

