import pyaudio
import numpy

class Settings:
    STREAMFORMAT = pyaudio.paFloat32
    DATAFORMAT = numpy.float32
    CHANNELS = 1  # Mono
    FREQUENCY = 48000  # Sampling rate (44.1kHz)
    SEGMENT_DURATION_MS = 100  # Segment duration in milliseconds
    frames_per_segment = int(FREQUENCY * SEGMENT_DURATION_MS / 1000)
    CHUNK_SIZE = frames_per_segment  # Size of each audio chunk

    # RECOGNIZER SETTINGS
    GMM_IS_TRAINED_DATA_TRESHOLD = 620 # 16 seconds of training are enough
    NUMBER_TRESHOLD = 30 # 0
    PERCENTAGE_TRESHOLD = 0.35
    MAKE_PLOTS = True 

    # Test Settings
    N_OF_RECOGNIZERS = 1