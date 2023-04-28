import numpy as np

from Settings import Settings
import numpy as np
import librosa
import librosa.feature
import numpy


class Sample:

    def __init__(self, ByteData, IsSpeech, TimeStamp):
        self.ByteData = ByteData
        self.IsSpeech = IsSpeech
        self.TimeStamp = TimeStamp
        self.Data = None
        self.Mfcc = None
        self.Mel = None
        self.Spect = None

    def __is_empty(self) -> bool:
        # Checks if there is lack of some data
        return self.Data is None or self.Mel is None
    
    def NormalizeMfcc(self):
        # Apllays process of nomalization on the Mfcc vector

        self.Mfcc = self.Mfcc.mean(axis=1)
        self.Mfcc = np.array_split(self.Mfcc, self.Mfcc.size)


    def GetMfcc(self):
        # Compute elements if needed
        if self.Data is None:
            self.ConvertData()

        test = True

        if test:
            self.Data = librosa.effects.preemphasis(self.Data)

        # Compute Mfcc component,
        self.Mfcc = librosa.feature.mfcc(y=self.Data, sr=Settings.FREQUENCY, window='hamming',
                                          n_mfcc=13, lifter=0, 
                                          n_fft=len(self.Data), htk=False, dct_type=2)
        
        self.NormalizeMfcc()
        



    def ConvertData(self):
        # Convert data from raw byte string and extract necessary information
        self.Data = np.frombuffer(self.ByteData, dtype=Settings.DATAFORMAT)
        self.Data = librosa.util.buf_to_float(self.Data)