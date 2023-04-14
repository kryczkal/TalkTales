from aud_process import *

SAVE_PATH = 'Out/'
LOAD_PATH = 'In/'


name = "44_pokoj_sofia_rode.wav"
name2 = "44_pokoj_sofia_samson.wav"



#Przykladowa inicjalizacja objektow dzwiekowych
#pliki sa szukane w LOAD_PATH i zapisywane w SAVE_PATH
#obj1 = aud(name)
#obj2 = aud_process.read_from_mic(5000)
#obj3 = aud(name2)


#Podzielenie objektu na kilka przedzialow czestotliwosci, zwraca tablice obiektow
#tab = obj1.split_to_freq_chunks((300, 1000, 3000))
#obj1.plot_all()


#zapis do pliku mozna w wywolaniu dodatkowo podac nazwe zapisu lub sciezke
#obj1.save_to_wav()


#Plotowanie wszystkich wykresow w jednym okienku
#obj2.plot_all()


#Obciecie przedzialu czasowego na podany w milisekundach
#obj2.change_interval(1500,3000)
#obj2.plot_db()


#Wyplotowanie wykresu podanego jako drugi argument po kolei z kazdego elementu podanej tablicy,
#Jesli trzeci argument jest true wyswietla kolejne wykresy w kolejnych okienkach
#plot_aud_array([obj1, obj2], 'all', True)