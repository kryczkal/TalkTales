import torch
import torchaudio

from queue import SimpleQueue
from ..diarization.Sample import VoiceSample
from Settings import Settings
from threading import Event
from ..diarization.Diarizer import Diarizer


def speaker_detector(input: SimpleQueue, output: SimpleQueue,
                     signals: dict[Event]):
    torchaudio.set_audio_backend("soundfile")
    torch.set_num_threads(1)
    vad, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad',
                                model='silero_vad',
                                force_reload=True)

    # Random Recongnizers
    recognizer = Diarizer(30, 0)

    # print("Recording audio... Press Ctrl+C to stop.")
    # byte_counter = 0
    timestamp_error = 0
    signals['ready'].set()
    while True:
        # print('speaker recognizer')
        byte_data = input.get()

        sample = VoiceSample(byte_data)
        tensor = torch.from_numpy(sample.data_convert())
        sample.speech_probability = vad(tensor, Settings.FREQUENCY).item()

        # if sample.speech_probability <= 0.60:
        #    print(f"speech probability: {sample.speech_probability}")
        if sample.speech_probability > 0.60:
            recognizer.append_data(sample.mfcc_get().T, timestamp_error)
            timestamp_error = 0
            recognizer.train()
            res = recognizer.check_for_speaker_change()
            if res:
                output.put(res)
            recognizer.is_the_model_trained()
        else:
            timestamp_error += Settings.SEGMENT_DURATION_MS / 1000
            # output.put(None)
