from aud_process import aud
from aud_process import plot_aud_array
from aud_process import save_aud_array
import aud_process

aud_process.SAVE_PATH = ''


name = "44_pokoj_sofia_rode.wav"
name2 = "44_pokoj_sofia_samson.wav"
signed16 = 'Signed-16-bit-PCM'
signed24 = 'Signed-24-bit-PCM'


obj1 = aud(name)


#TODO:
# odszumianie aproksymacja liniowa lub filtry przepustowe
# poprawic integralnosc
# dodaj opisy
# sprawdz w akcji - strumienie
# popraw wyswietlanie wykresow - dodaj mozliwosc wyswietlenie konretnego przedzialu czasowego
# dodaj odczyt z mikrofonu
# 