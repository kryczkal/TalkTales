import io
import speech_recognition as sr
import whisper_timestamped as whisper
import torch

from os import path
from datetime import datetime, timedelta
from queue import Queue, SimpleQueue
from tempfile import NamedTemporaryFile
from time import sleep
from settings import Settings
from threading import Event


def speech_to_text(source: sr.AudioSource,
                   output: SimpleQueue,
                   signals: dict[Event]):
    # The last time a recording was retreived from the queue.
    phrase_time = None
    # Current raw audio bytes.
    last_sample = bytes()
    # Thread safe Queue for passing data
    # from the threaded recording callback.
    data_queue = Queue()
    # We use SpeechRecognizer to record our audio because
    # it has a nice feauture where it can detect when speech ends.
    recorder = sr.Recognizer()
    recorder.energy_threshold = Settings.ENERGY_THRESHOLD
    # Definitely do this, dynamic energy compensation
    # lowers the energy threshold dramtically to a point
    # where the SpeechRecognizer never stops recording.
    recorder.dynamic_energy_threshold = False

    mic_source = sr.Microphone(sample_rate=Settings.FREQUENCY,
                               chunk_size=Settings.CHUNK_SIZE // 4)
    # Load / Download model
    model = Settings.MODEL
    # Allow loading english-only models
    if Settings.LANGUAGE == 'en':
        model += '.en'
    # If model fails to be fetched (e.g. the machine is offline),
    # look for it on disk
    try:
        audio_model = whisper.load_model(model)
    except Exception:
        model = path.expanduser(f'~/.cache/whisper/{model}.pt')
        audio_model = whisper.load_model(model)

    record_timeout = Settings.RECORD_TIMEOUT
    phrase_timeout = Settings.PHRASE_TIMEOUT

    temp_file = NamedTemporaryFile().name
    transcription = ['']

    with mic_source:
        recorder.adjust_for_ambient_noise(mic_source)

    def record_callback(_, audio: sr.AudioData) -> None:
        """Threaded callback function to receive audio data
        when recordings finish.

        audio: An AudioData containing the recorded bytes.
        """
        # Grab the raw bytes and push it into the thread safe queue.
        data = audio.get_raw_data()
        data_queue.put(data)

    # Create a background thread that will pass us raw audio bytes.
    # We could do this manually
    # but SpeechRecognizer provides a nice helper.
    recorder.listen_in_background(source,
                                  record_callback,
                                  phrase_time_limit=record_timeout)

    # Cue the user that we're ready to go.
    # print("Model loaded.\n")
    signals['ready'].set()
    transcription_start = datetime.utcnow()
    phrase_start = datetime.utcnow()
    while True:
        # print('speech to text')
        try:
            now = datetime.utcnow()
            # Pull raw recorded audio from the queue.
            if not data_queue.empty():
                phrase_complete = False
                # If enough time has passed between recordings,
                # consider the phrase complete. Clear the current
                # working audio buffer to start over with the new data.
                if (phrase_time and now - phrase_time
                        > timedelta(seconds=phrase_timeout)):
                    last_sample = bytes()
                    phrase_complete = True
                    phrase_start = datetime.utcnow()
                # This is the last time we received
                # new audio data from the queue.
                phrase_time = now

                # Concatenate our current audio data
                # with the latest audio data.
                while not data_queue.empty():
                    data = data_queue.get()
                    last_sample += data

                # Use AudioData to convert the raw data to wav data.
                audio_data = sr.AudioData(last_sample,
                                          source.SAMPLE_RATE,
                                          source.SAMPLE_WIDTH)
                wav_data = io.BytesIO(audio_data.get_wav_data())

                # Write wav data to the temporary file as bytes.
                with open(temp_file, 'w+b') as f:
                    f.write(wav_data.read())

                # Read the transcription.
                result = whisper.transcribe(audio_model, temp_file,
                                            fp16=torch.cuda.is_available(),
                                            language=Settings.LANGUAGE)
                # text = result['text'].strip()
                # prototyp timestamp
                text = []
                if result['segments']:
                    for i in result['segments']:
                        for j in i['words']:
                            diff = phrase_start + timedelta(seconds=j['start'])
                            diff -= transcription_start
                            text.append((
                                diff.seconds + diff.microseconds / 1000000,
                                j['text'].strip()
                            ))

                # If we detected a pause between recordings,
                # add a new item to our transcripion.
                # Otherwise edit the existing one.
                if phrase_complete:
                    # print(transcription)
                    for i in transcription:
                        output.put(i)
                transcription = text

                # Clear the console to reprint
                # the updated transcription.
                # os.system('cls' if os.name == 'nt' else 'clear')
                # for line in transcription:
                #     print(line)
                # Flush stdout.
                # print('', end='', flush=True)

                # Infinite loops are bad for processors, must sleep.
                sleep(0.25)
        except KeyboardInterrupt:
            break

    print("\n\nTranscription:")
    for line in transcription:
        print(line)


if __name__ == "__main__":
    speech_to_text()
