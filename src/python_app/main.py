from queue import Queue, SimpleQueue, Empty
from threading import Thread

from speechtotext import stt
from voice_recognition import voicerecognition
from audioproducer import produce

# inputs of audio processors
stt_audio = Queue()
voice_rec_audio = Queue()
# outputs of audio processors
stt_data = SimpleQueue()
voice_rec_data = SimpleQueue()

if __name__ == '__main__':
    audio_thread = Thread(target=produce, args=([stt_audio, voice_rec_audio]))
    stt_thread = Thread(target=stt, args=(stt_audio, stt_data))
    voice_rec_thread = Thread(target=voicerecognition, args=(voice_rec_audio, voice_rec_data))
    
    stt_packet = ('', 0.0)
    voice_rec_packet = None
    speaker = 0
    # main loop
    while True:
        try:
            stt_packet = stt_data.get()
        except Empty:
            continue # no new data from stt
        
        try:
            voice_rec_packet = voice_rec_data.get()
        except Empty:
            voice_rec_packet = None # no new data from voice classifier
        if voice_rec_packet and stt_packet[1] >= voice_rec_packet[1]:
            speaker = voice_rec_packet[0]
        
        ... # grab the stt_data and voice_rec_data information