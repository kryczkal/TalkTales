from settings import Settings
import librosa
import librosa.feature

class Sample:
    def __init__(self, data):
        self.data = data
    
    def get_mfccs(self):
        self.mfccs = librosa.feature.mfcc(self.data, Settings.FREQUENCY, 40)
        return self.mfccs
    
