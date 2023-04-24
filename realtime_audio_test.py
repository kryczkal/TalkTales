from aud_process import aud
from aud_process import save_aud_array
from aud_process import plot_aud_array
from aud_process import read_from_mic
from aud_process import save_plot_aud_array
from aud_process import standard_filter
import aud_process
import os
import librosa as lib
import matplotlib.pyplot as plt
from scipy.signal import lfilter
import numpy as np
import webrtcvad

aud_process.SAVE_PATH = 'Out/'
aud_process.LOAD_PATH = 'In/TODO/'
vad = webrtcvad.Vad(1)

Sofianame = "44_pokoj_sofia_rode.wav"
Kubaname = "44_pokoj_kuba_rode.wav"
Lukaszname = "44_pokoj_lukasz_rode.wav"
Ernestname = "44_pokoj_ernest_rode.wav"

MateuszName = "44_dworzec_MAteusz_samson.wav"
name = "44_metro_lukasz_samson.wav"

Kuba = aud(Kubaname)
Kuba = Kuba.split_to_time_chunks((40,44))
Ernest = aud(Ernestname)
Ernest = Ernest.split_to_time_chunks((24.5,26))
Sofia = aud(Sofianame)
# Sofia = standard_filter(Sofia)

Sofia = Sofia.split_to_time_chunks((17,20))
Sofia = Sofia.split_to_windows(100,50)

Kuba = Kuba.split_to_windows(100,50)
Ernest = Ernest.split_to_windows(100,50)

Ernest = Ernest[:25]

Sofia = Sofia[:25]
Sofia = Sofia + Ernest

for i in range(49):
    plt.subplot(7,7, i+1)
    Sofia[i].setup_mfcc_plot()

Sofia[0].plot()



num = 8
# plot_aud_array([Sofia[num], Kuba[num], Ernest[num]], 'mfcc', True)

# obj2 = aud_process.standard_filter(obj1)

#obj3 = aud(lib.effects.harmonic(obj2.data), obj2.freq)
#obj3.save_to_wav("Harmonic")

# plot_aud_array([obj1, obj5], 'all', True)

#TODO:
#-Plot patterns do plot_aud_array
#-poprawic zapisywanie
#-funkcja na partioning