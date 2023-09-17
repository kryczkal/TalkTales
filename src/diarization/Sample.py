import numpy as np
import librosa
import librosa.feature
import pyaudio as py
import warnings

from ..Settings import Settings
warnings.filterwarnings("ignore")

# used in speech tests
import torch
import torchaudio

# TODO CONSIDER RUNNING IN PARALLEL 

class VoiceSample:
    """
    Class used to represent a single audio sample. Contains raw byte data, converted data, \n
    timestamp of object creation and methods to calculate mfcc of the sample.
    """
 
    # Vad settings used in spech probability tests
    # Here u can inject whatever vad module u want to use
    torchaudio.set_audio_backend("soundfile")
    torch.set_num_threads(1)
    vad, _ = torch.hub.load(repo_or_dir='snakers4/silero-vad',
                                model='silero_vad',
                                force_reload=True)
    
    # WARNING - fast workaround
    silent_seconds = 0

    def __init__(self, byte_data: bytes):
        """
        Initializes VoiceSample class with byte formatted audio data,
        is_speech flag indicating where audio has speech or not, and 
        timestamp of the object.
        """
        self.byte_data = byte_data
        self.data = None
        self.mfcc = None
        self.speech_probability = None
    
    def __get_speech_prob(self) -> float:
        tensor = torch.from_numpy(self.data_convert())
        self.speech_probability = self.vad(tensor, Settings.FREQUENCY).item()
        
        return self.speech_probability

    def if_is_speech(self) -> bool:
        self.__get_speech_prob()

        if self.speech_probability < Settings.SPEECH_PROB_THRESHOLD:
            self.silent_seconds += Settings.SEGMENT_DURATION_S
            return False
        else:
            self.silent_seconds = 0
            return True


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
            self.data = self.data.astype(Settings.DATA_FORMAT, order='C') / Settings.DATA_FORMAT(Settings.MAX_INT16)
            
        return self.data