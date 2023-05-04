import numpy as np
import librosa
import librosa.feature
import webrtcvad

from Settings import Settings
Vad = webrtcvad.Vad(1)

class VoiceSample:
    def __init__(self, byte_data, is_speech, time_stamp):
        self.byte_data = byte_data
        self.time_stamp = time_stamp
        self.is_speech = is_speech
        self.data = None
        self.mfcc = None
        self.mel = None


    def __is_empty(self) -> bool:
        # Checks if there is lack of some data
        return self.data is None or self.mel is None
    
    def mfcc_get(self):
        # Compute elements if needed
        if self.__is_empty():
            self.data_convert()

        # Compute Mfcc component
        self.mfcc = librosa.feature.mfcc(y=self.data, S=self.mel, sr=Settings.FREQUENCY,
                                          n_mfcc=13, fmin=100, fmax=8000, lifter=1,
                                          n_fft=len(self.data))
        return self.mfcc
    
    def data_convert(self):
        # Convert data from raw byte string and extract necessary information
        self.data = np.frombuffer(self.byte_data, dtype=Settings.DATAFORMAT).astype(np.float32, order='C') / 32768.0