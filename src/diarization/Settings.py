import pyaudio
import numpy

class Settings:
    STREAM_FORMAT = pyaudio.paFloat32
    DATA_FORMAT = numpy.float32
    CHANNELS = 1  # Mono channel support only
    FREQUENCY = 48000  # Sampling rate (44.1kHz)
    SEGMENT_DURATION_MS = 100  # Segment duration in milliseconds
    FRAMES_PER_SEGMENT = FREQUENCY * SEGMENT_DURATION_MS // 1000 # Segment expressed in frames (single data unit)   

    # RECOGNIZER SETTINGS
    GMM_IS_TRAINED_DATA_TRESHOLD = 1620 # 16 seconds of training are enough
    NUMBER_TRESHOLD = 25 # 0
    PERCENTAGE_THRESHOLD = 0.20

    # Test Settings
    N_OF_RECOGNIZERS = 3
    MAKE_PLOTS = True 
    RECOGNIZER_LOG_SPEAKER_CHANGE = True