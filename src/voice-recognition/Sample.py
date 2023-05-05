import numpy as np
import librosa
import librosa.feature

from Settings import Settings

class VoiceSample:
    """
    Class used to represent a single audio sample. Contains raw byte data, converted data, \n
    timestapt of creation of the object and methods to calculate mfcc of the sample.
    """
    def __init__(self, byte_data, is_speech, time_stamp):
        """
        Initializes VoiceSample class with byte formatted audio data,
        is_speech flag indicating where audio has speech or not, and 
        timestamp of the object.
        """
        self.byte_data = byte_data
        self.time_stamp = time_stamp
        self.is_speech = is_speech
        self.data = None
        self.mfcc = None
    
    def mfcc_get(self):
        """
        Computes and returns Mfcc components of audio data.
        """

        # Compute elements if needed
        if self.data is None:
            self.data_convert()

        # Compute Mfcc component
        self.mfcc = librosa.feature.mfcc(y=self.data, sr=Settings.FREQUENCY,
                                          n_mfcc=13, fmin=100, fmax=8000, lifter=1,
                                          n_fft=len(self.data))
        return self.mfcc
    
    def data_convert(self):
        """
        Converts audio data from byte format, rescales it, and
        converts it to float32 format.
        """
                
        # Convert data from raw byte string and extract necessary information
        self.data = np.frombuffer(self.byte_data, dtype=Settings.DATAFORMAT).astype(np.float32, order='C') / 32768.0