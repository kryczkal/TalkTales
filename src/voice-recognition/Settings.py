import pyaudio
import numpy

class Settings:

    STREAMFORMAT = pyaudio.paInt16  # Audio format (32-bit floats)
    DATAFORMAT = numpy.int16
    CHANNELS = 1  # Mono
    FREQUENCY = 48000  # Sampling rate (44.1kHz)
    SEGMENT_DURATION_MS = 10  # Segment duration in milliseconds
    frames_per_segment = int(FREQUENCY * SEGMENT_DURATION_MS / 1000)
    CHUNK_SIZE = frames_per_segment  # Size of each audio chunk

    #* changes for VAD:
    #pa.Int16
    #48000
    #30