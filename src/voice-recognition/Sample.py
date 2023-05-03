import numpy as np

from Settings import Settings
import numpy as np
import librosa
import librosa.feature
import numpy


class Sample:
    def concatenate_data(self, s):
        self.Data = numpy.concatenate((self.Data, s.Data), axis=None)
        return self


    def __init__(self, ByteData, IsSpeech, TimeStamp):
        self.ByteData = ByteData
        self.IsSpeech = IsSpeech
        self.TimeStamp = TimeStamp
        self.Data = None
        self.Mfcc = None
        self.Mel = None

    def __is_empty(self) -> bool:
        # Checks if there is lack of some data
        return self.Data is None or self.Mel is None

    def GetMfcc(self):
        # Compute elements if needed
        if self.__is_empty():
            self.ConvertData()

        # Compute Mfcc component
        self.Mfcc = librosa.feature.mfcc(y=self.Data, S=self.Mel, sr=Settings.FREQUENCY,
                                          n_mfcc=13, fmin=100, fmax=8000, lifter=1,
                                          n_fft=len(self.Data))
        return self.Mfcc

    def ConvertData(self):
        # Convert data from raw byte string and extract necessary information
        self.Data = np.frombuffer(self.ByteData, dtype=Settings.DATAFORMAT).astype(np.float32, order='C') / 32768.0
        # self.Mel = librosa.feature.melspectrogram(y=self.Data, sr=Settings.FREQUENCY, dtype=Settings.DATAFORMAT)
        # TODO Problem jest tutaj jakis
