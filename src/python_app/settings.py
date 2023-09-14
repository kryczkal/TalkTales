import pyaudio
import numpy


class Settings:
    STREAM_FORMAT = pyaudio.paInt16
    DATA_FORMAT = numpy.float32
    CHANNELS = 1  # Mono channel support only
    FREQUENCY = 48000  # Sampling rate (48kHz)
    SEGMENT_DURATION_MS = 100  # Segment duration in milliseconds
    FRAMES_PER_SEGMENT = FREQUENCY * SEGMENT_DURATION_MS // 1000 # Segment expressed in frames (single data unit)

    # RECOGNIZER SETTINGS
    GMM_IS_TRAINED_DATA_THRESHOLD = 1620  # 16 seconds of training are enough
    NUMBER_THRESHOLD = 30  # 0
    PERCENTAGE_THRESHOLD = 0.35
