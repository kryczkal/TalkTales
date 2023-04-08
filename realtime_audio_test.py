from aud_process import aud
from aud_process import plot_aud_array
from aud_process import save_aud_array

name = "44_pokoj_sofia_rode.wav"
name2 = "44_metro_sofia_rode.wav"

obj1 = aud(name)
obj1.save_to_wav()


tab = obj1.split_to_chunks((0,500,1500,3000,6000))

tab[0].save_to_wav()

# save_aud_array(tab)
# plot_aud_array(tab)



# obj2 = tab[3] + tab[2] + tab[1] + tab[0]

# obj2.setup_def_plot()
# obj2.plot()

#TODO:
#-potrzebne operacje
#-odszumianie aproksymacja liniowa lub filtry przepustowe
#-popraw to co jest
#-dodaj opisy
#-sprawdz w akcji - strumienie
