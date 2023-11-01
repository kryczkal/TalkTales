import pyaudio
import os
from tqdm import tqdm
from src.Settings import Settings
from src.diarization.Diarizer import Diarizer

"""
    This file is used to invoke Diarizers components without application frontend.
    It's helpful to debug and test some changes and new features added to the class.

    There are two modes possible, changed using READ_FROM_FILE variable:
    - True: reads WAV file from disks and analyse its content
    - False: tries to find system sound input and reads bytes from it, putting it info diarizer pipeline
"""

READ_FROM_FILE = True
filename = 'assets/nag2.wav'

time_start = 0
audio = pyaudio.PyAudio()

diarizer = Diarizer()

if READ_FROM_FILE:

    filesize = os.path.getsize(filename)

    with open(filename, 'rb') as wav:

        # IDK how wav headers works, but without this line it's not working correctly
        header = wav.read(100)

        byte_data = True
        num_chunks = filesize // Settings.FRAMES_PER_SEGMENT / 4
        wav_data = wav.read()

else:
    stream = audio.open(format=Settings.STREAM_FORMAT,
                        channels=Settings.CHANNELS,
                        rate=Settings.FREQUENCY,
                        input=True,
                        frames_per_buffer=Settings.FRAMES_PER_SEGMENT)

    if stream is None:
        exit(1)

try:
    print("Recording audio... Press Ctrl+C to stop.")
    byte_counter = 0
    silent_seconds = 0
    if READ_FROM_FILE:
        with tqdm(total=num_chunks) as pbar:
            while byte_data:
                byte_data = wav_data[byte_counter * 4 * Settings.FRAMES_PER_SEGMENT:
                                     (byte_counter + 1) * 4 * Settings.FRAMES_PER_SEGMENT]
                byte_counter += 1
                if len(byte_data) < 4 * Settings.FRAMES_PER_SEGMENT:
                    byte_data = False
                    break
                pbar.update(1)

                diarizer.diarize(byte_data)
    else:
        while True:
            byte_data = stream.read(Settings.FRAMES_PER_SEGMENT)
            diarizer.diarize(byte_data)

except KeyboardInterrupt:
    print("Stopped recording")
except IndexError:
    print("IndexError")
except ValueError:
    print("ValueError - end of file")
finally:
    pass

if Settings.MAKE_PLOTS:
    diarizer.plot()
