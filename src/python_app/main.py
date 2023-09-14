from queue import SimpleQueue
from threading import Thread, Event
from time import sleep
from bisect import insort
from ansicolors import color, reset

import os

from speechtotext import speech_to_text
from speakerrecognizer import speaker_detector
from audioproducer import produce_audio

# inputs of audio processors, simple byte data
speech_text_audio = SimpleQueue()
voice_rec_audio = SimpleQueue()
# outputs of audio processors, processed abstract data
speech_text_data = SimpleQueue()
voice_rec_data = SimpleQueue()
# daemon ready event
st_ready = Event()
vr_ready = Event()
st_stop = Event()
vr_stop = Event()


if __name__ == '__main__':

    # Produces raw bytes data and sends it to corresponding queue
    audio_thread = Thread(
        target=produce_audio,
        args=(speech_text_audio, voice_rec_audio, {}),
        name='audio_producer',
        daemon=True
    )

    # Process raw byte data into text, using desired model
    speech_text_thread = Thread(
        target=speech_to_text,
        args=(speech_text_audio, speech_text_data, {
            'ready': st_ready,
            'stop': st_stop
        }),
        name='stt',
        daemon=True
    )

    # Process raw byte data into packets consisting of timestamps and speaker flags
    voice_rec_thread = Thread(
        target=speaker_detector,
        args=(voice_rec_audio, voice_rec_data, {
            'ready': vr_ready,
            'stop': vr_stop
        }),
        name='voice_rec',
        daemon=True
    )

    speech_text_thread.start()
    voice_rec_thread.start()

    st_ready.wait()
    vr_ready.wait()

    audio_thread.start()

    speech_text_packet = ('', 0.0)
    voice_rec_packet = None
    transcription = []
    rewrite = False
    curr_color = 1

    def key(x: tuple):
        return x[0]
    
    # Writes console with correct color
    def rewrite_console(curr_color: int, transcription: list):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(color(curr_color + 1))
        for i in transcription:
            if isinstance(i[1], str):
                print(i[1])
            else:
                print(color(1 + (curr_color := not curr_color)))
    
    # Main loop, no computation here. Only writes console with results.
    # In future this will be main interface backend - frontend
    while True:
        try:
            sleep(0.25)
            if not speech_text_data.empty():
                while not speech_text_data.empty():
                    speech_text_packet = speech_text_data.get()
                    insort(transcription, speech_text_packet, key=key)
                rewrite = True
            if not voice_rec_data.empty():
                voice_rec_packet = (voice_rec_data.get(), True)
                insort(transcription, voice_rec_packet, key=key)
                rewrite = True
            if rewrite:
                rewrite_console(curr_color, transcription)
                rewrite = False
        # stt_packet = stt_data.get()
        # voice_rec_packet = voice_rec_data.get()
        # print(stt_packet)
        # print(voice_rec_packet)
        # if stt_packet:
        #     print(f'{color(voice_rec_packet + 2)}{stt_packet}{reset()}')

        # ...  # do sth with the speaker id and correct word/sentence
        except KeyboardInterrupt:
            print(reset())
            break