from settings import Settings
import librosa
import librosa.feature

class Sample:
    def __init__(self, data):
        self.data = data
        self.mfcc = 0

    def get_mfccs(self):
        self.mfccs = librosa.feature.mfcc(y=self.data, sr=Settings.FREQUENCY, n_mfcc=40)
        return self.mfccs
    
