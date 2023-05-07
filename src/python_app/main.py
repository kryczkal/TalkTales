from queue import SimpleQueue
from threading import Thread, Event

# from ansicolors import color, reset

import micstream as ms

from speechtotext import speech_to_text
from speakerrecognizer import speaker_detector
from audioproducer import produce_audio

# inputs of audio processors
stt_audio = SimpleQueue()
voice_rec_audio = SimpleQueue()
# outputs of audio processors
stt_data = SimpleQueue()
voice_rec_data = SimpleQueue()
# daemon ready event
stt_ready = Event()
sr_ready = Event()

source = ms.RemoteStreamSource(stt_audio)  # TODO

if __name__ == '__main__':

    audio_thread = Thread(
        target=produce_audio,
        args=(stt_audio, voice_rec_audio),
        name='audio_producer',
        daemon=True
    )
    stt_thread = Thread(
        target=speech_to_text,
        args=(source, stt_data, {
            'ready': stt_ready
        }),
        name='stt',
        daemon=True
    )
    voice_rec_thread = Thread(
        target=speaker_detector,
        args=(voice_rec_audio, voice_rec_data, {
            'ready': sr_ready
        }),
        name='voice_rec',
        daemon=True
    )

    stt_thread.start()
    voice_rec_thread.start()

    stt_ready.wait()
    sr_ready.wait()

    audio_thread.start()

    stt_packet = ('', 0.0)
    voice_rec_packet = None
    # main loop
    while True:
        stt_packet = stt_data.get()
        voice_rec_packet = voice_rec_data.get()
        # print(stt_packet)
        # print(voice_rec_packet)
        # if stt_packet:
        #     print(f'{color(voice_rec_packet + 2)}{stt_packet}{reset()}')

        # ...  # do sth with the speaker id and currect word/sentence
