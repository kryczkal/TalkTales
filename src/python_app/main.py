from queue import Queue, SimpleQueue
from threading import Thread

from ansicolors import color, reset

from speechtotext import stt
from voicerecognition import voice_recognition
from audioproducer import produce_audio

# inputs of audio processors
stt_audio = Queue()
voice_rec_audio = Queue()
# outputs of audio processors
stt_data = SimpleQueue()
voice_rec_data = SimpleQueue()

if __name__ == '__main__':

    audio_thread = Thread(
        target=produce_audio,
        args=([stt_audio, voice_rec_audio],),
        name='audio_producer',
        daemon=True
    )
    stt_thread = Thread(
        target=stt,
        args=(stt_audio, stt_data),
        name='stt',
        daemon=True
    )
    voice_rec_thread = Thread(
        target=voice_recognition,
        args=(voice_rec_audio, voice_rec_data),
        name='voice_rec',
        daemon=True
    )

    audio_thread.start()
    stt_thread.start()
    voice_rec_thread.start()

    stt_packet = ('', 0.0)
    voice_rec_packet = None
    # main loop
    while True:
        stt_packet = stt_data.get()
        voice_rec_packet = voice_rec_data.get()

        if stt_packet:
            print(f'{color(voice_rec_packet + 2)}{stt_packet}{reset()}')

        ...  # do sth with the speaker id and currect word/sentence
