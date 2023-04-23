import pyaudio

class Settings:
    CHUNK_SIZE = 1024  # Size of each audio chunk
    FORMAT = pyaudio.paFloat32  # Audio format (32-bit floats)
    CHANNELS = 1  # Mono
    FREQUENCY = 44100  # Sampling rate (44.1kHz)
    SEGMENT_DURATION_MS = 20  # Segment duration in milliseconds
    frames_per_segment = int(FREQUENCY * SEGMENT_DURATION_MS / 1000)