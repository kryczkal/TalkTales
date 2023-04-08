from aud_process import aud
from aud_process import plot_aud_array

name = "44_pokoj_sofia_rode.wav"
name2 = "44_metro_sofia_rode.wav"

obj1 = aud(name2)

tab = obj1.split_to_chunks((0,500,1500,3000,6000))
# plot_aud_array(tab, 'mel')


obj2 = tab[3] + tab[2] + tab[1] + tab[0]

obj2.setup_def_plot()
obj2.plot()

#TODO:
#-zapis do pliku
#-potrzebne operacje
#-odszumianie aproksymacja liniowa lub filtry przepustowe
#-popraw to co jest
#-dodaj opisy
#-sprawdz w akcji - strumienie
#-konkatenacja buffer
