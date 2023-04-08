# Projekt_audio_processing
 interfejs do analizy pod projekt z PTI


1) objekt musi byc zainicjalizowany na jeden z dwoch sposobow:
   a) Podać nazwe/sciezke do pliku z ktorego zostanie pobrane audio
   b) Jako dwa argumenty, pierwszy - probki dzwieku, drugi czestotliwosc probkowania
   
2) objekt moze wyswietlac wybrane wykresy. Robimy to w nastepujacy sposob:
   objekt.setup_plot_fourier() - przygotowuje wykres amplitudy od czestotliwosci w zakresie od 0 - x
   objekt.setup_def_plot() - przygotowuje wykres amplitudy bitowej (podstawowy wykres) od czasu
   objekt.setup_db_plot(window) - przygotowuje wykres amplitudy w db od czasu, parametr windows okresa dziedzine wykresu, a dokladnie na jakich odcinkach bedzie obliczana energia (UWAGA - zweryfikowac)
   objekt.setup_mel_plot(window, overlap) - przygotowuje wkyres spektogramu, gdzie window to samo co wyzej, oraz overlap to samo co window tylko w dziedzinie       czestotliwosci (nie jestem do konca pewien)
   
   Po przygotowaniu wykresu wywolujemy objekt.plot()
   
3) Przygotowane są metody do przeprowadzania odpowiednich obliczń
 
4) Metoda objekt.split_to_chunks((x1, x2 ,x3, ...)) zwraca tablice klass aud ktore reprezentuja rozbite bazowe audio na podane przedzialy czestotliwosci np:
  
  
    tab = obj1.split_to_chunks((0,500,1500,3000,6000)) - rozbija audio na 4 sciezki z przedzialow czestotliwosc: 0-500, 500-1500, 1500-3000, 3000-6000
    
    TODO:optymalizacja
    
5) objekt1 << objekt2 kopiowanie plikow audio

6) objekt1 + objekt2 - zwraca dodawanie składowych plików audio w dziedzinie czestotliwosci - objekty musza miec taka sama ilosc probek, ta sama czestotliwosc probkowania TODO: optymalizacja dodawania przez zapisywanie odpowiedniej dziedziny czestotliwosci i jej rozwijania

7)Funkcja plot_aud_array(tab, plot_type) - wyswietla odpowiednio ulozone wykresy objektow z tablicy tab, gdzie wykresy są okreslone stringiem podanym jako 2 argument
 plot_type = "def", "mel", "db", "fourier"
 
 
