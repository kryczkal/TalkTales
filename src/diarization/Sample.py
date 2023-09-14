import numpy as np
import librosa
import librosa.feature
import pyaudio as py
from ..Settings import Settings
import warnings
warnings.filterwarnings("ignore")

# TODO CONSIDER RUNNING IN PARALLEL 

class VoiceSample:
    """
    Class used to represent a single audio sample. Contains raw byte data, converted data, \n
    timestamp of object creation and methods to calculate mfcc of the sample.
    """
    def __init__(self, byte_data: bytes, is_speech: float = None, time_stamp: int = None):
        """
        Initializes VoiceSample class with byte formatted audio data,
        is_speech flag indicating where audio has speech or not, and 
        timestamp of the object.
        """
        self.byte_data = byte_data
        self.time_stamp = time_stamp
        self.speech_probability = is_speech
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
        self.mfcc = librosa.feature.mfcc(y = self.data,
                                         sr = Settings.FREQUENCY,
                                         n_mfcc = Settings.MFCC_COMPONENTS,
                                         fmin = Settings.MFCC_MIN_INPUT_FREQ, 
                                         fmax = Settings.MFCC_MAX_INPUT_FREQ, 
                                         lifter = 1,
                                         n_fft = Settings.MFCC_WINDOW_SIZE
                            ) 
        return self.mfcc
    
    def data_convert(self):
        """
        Converts audio data from byte format, rescales it, and
        converts it to float32 format.
        """
                
        # Convert data from raw byte string and extract necessary information
        self.data = np.frombuffer(self.byte_data, dtype=Settings.DATA_FORMAT)

        if Settings.STREAM_FORMAT == py.paInt16: # <-------------------------- TODO
            self.data = self.data.astype(np.float32, order='C') / np.float32(Settings.MAX_INT16)
            
        return self.data