import pyaudio
import numpy


class Settings:
    STREAMFORMAT = pyaudio.paFloat32
    DATAFORMAT = numpy.float32
    CHANNELS = 1  # Mono
    FREQUENCY = 48000  # Sampling rate (48kHz)
    SEGMENT_DURATION_MS = 100  # Segment duration in milliseconds
    frames_per_segment = int(FREQUENCY * SEGMENT_DURATION_MS / 1000)
    CHUNK_SIZE = frames_per_segment  # Size of each audio chunk

    # RECOGNIZER SETTINGS
    GMM_IS_TRAINED_DATA_TRESHOLD = 1620  # 16 seconds of training are enough
    NUMBER_TRESHOLD = 30  # 0
    PERCENTAGE_TRESHOLD = 0.35

    # SPEECH TO TEXT SETTINGS
    # model_choices=["tiny", "base", "small", "medium", "large"])
    MODEL = 'small'
    LANGUAGE = 'pl'
    ENERGY_THRESHOLD = 1000
    RECORD_TIMEOUT = 2
    PHRASE_TIMEOUT = 3
