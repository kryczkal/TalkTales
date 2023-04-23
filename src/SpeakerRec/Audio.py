import librosa
import librosa.feature
from typing import Optional
import webrtcvad
class Audio:

    def __init__(self, path):
        [y, fs] = librosa.load(path)
        self.__mfccs = librosa.feature.mfcc(y=y, sr=fs, n_mfcc=20)

    def get_mfcc(self):
        return self.__mfccs
    def preprocess(path,
                   source_sr: Optional[int] = None,
                   normalize : Optional[bool] = True):
        y, sr = librosa.load(str(path))
        #do dokonczenia
