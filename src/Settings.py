import pyaudio
import numpy

class Settings:
    # --------------------------
    # Audio data information
    # --------------------------
    
    # WARNING 
    
    STREAM_FORMAT = pyaudio.paFloat32
    DATA_FORMAT = numpy.float32
    CHANNELS = 1  # Mono channel support only
    FREQUENCY = 48000  # Sampling rate (44.1kHz)
    SEGMENT_DURATION_MS = 100  # Segment duration in milliseconds
    FRAMES_PER_SEGMENT = FREQUENCY * SEGMENT_DURATION_MS // 1000 # Segment expressed in frames (single data unit)
    MAX_INT16 = 32768
    
    # --------------------------
    # Mfcc generation paremeters
    # --------------------------

    MFCC_COMPONENTS = 13
    MFCC_MIN_INPUT_FREQ = 100
    MFCC_MAX_INPUT_FREQ = 8000
    MFCC_WINDOW_SIZE = int(FREQUENCY / 100)

    # --------------------------
    # Diarization module settings
    # --------------------------
    
    # RECOGNIZER SETTINGS
    MAXIMUM_TRAINING_INTERVAL = 16 # in seconds
    MINIMAL_TRAINING_INTERVAL = 3 # in seconds
    
    MINIMAL_TRAINING_INTERVAL_SEGMENTS = MINIMAL_TRAINING_INTERVAL * 1000 // SEGMENT_DURATION_MS
    MAXIMUM_TRAINING_INTERVAL_SEGMENTS = MAXIMUM_TRAINING_INTERVAL * 1000 // SEGMENT_DURATION_MS
    MFCC_PER_SEGMENT = SEGMENT_DURATION_MS // 10 # Number of mfcc vectors we get from one speech segment 
    
    MFCC_MAX_SIZE = MFCC_PER_SEGMENT * MAXIMUM_TRAINING_INTERVAL_SEGMENTS
    MFCC_MIN_SIZE = MFCC_PER_SEGMENT * MINIMAL_TRAINING_INTERVAL_SEGMENTS

    # Parameters that set the magnitude of divergence required to consider the current speaker a "new" one 
    NUMBER_THRESHOLD = 25 # 0
    PERCENTAGE_THRESHOLD = 0.20

    # --------------------------
    # Debugging settings
    # --------------------------
    
    N_OF_RECOGNIZERS = 1
    MAKE_PLOTS = True 
    RECOGNIZER_LOG_SPEAKER_CHANGE = True
    
    # --------------------------
    # No idea 
    # --------------------------
    # 48000/100 (1/100 = 10/1000) okienko - 10 ms, 1000ms to sekunda