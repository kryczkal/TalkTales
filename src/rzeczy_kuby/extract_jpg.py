from aud_process import aud
from aud_process import save_aud_array
from aud_process import plot_aud_array
from aud_process import read_from_mic
from aud_process import save_plot_aud_array
import aud_process
import os
import librosa as lib
import matplotlib.pyplot as plt

aud_process.SAVE_PATH = 'Out/'
aud_process.LOAD_PATH = 'In/TODO/'


for num, names in enumerate(os.listdir(aud_process.LOAD_PATH)):
    obj2 = aud_process.standard_filter(aud(names))
    obj1 = aud(names)
    obj1.name = names[:-4] + "_input"
    obj2.name = names[:-4] + "_output"
    obj2.save_to_wav("Out/"+obj2.name)
    
    plt.subplot(2,3,1)
    obj1.setup_def_plot()
    plt.subplot(2,3,2)
    obj1.setup_fourier_plot()
    plt.subplot(2,3,3)
    obj1.setup_mel_plot()
    plt.subplot(2,3,4)
    obj2.setup_def_plot()
    plt.subplot(2,3,5)
    obj2.setup_fourier_plot()
    plt.subplot(2,3,6)
    obj2.setup_mel_plot()

    figure = plt.gcf() 
    figure.set_size_inches(19, 10)

    plt.savefig( "C:/Users/Jlisowskyy/Desktop/PTI/AUD/Projekt_audio_processing/JPEGS/" + str(obj1.name) + '.jpg', dpi=100)
    plt.close()