from Settings import Settings
import librosa
import librosa.feature

class Sample:
    def __init__(self, data):
        self.data = data
        self.mfcc = 0

    def get_mfccs(self):
        self.mfcc = librosa.feature.mfcc(y=self.data, sr=Settings.FREQUENCY, n_mfcc=13, fmin=100, fmax=8000, lifter=1)

    
