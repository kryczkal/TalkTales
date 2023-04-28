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


Sofianame = "44_pokoj_sofia_rode.wav"

test = aud(Sofianame)

count = int(test.duration / 0.5)
tab = []
for i in range(count):
    tab.append(float(i*0.5))
tab.append(test.duration)

tabik = test.split_to_time_chunks(tab)


for i in range(len(tabik)):
    tabik[i] = aud_process.standard_filter(tabik[i])

for i in range(len(tabik)-1):
    tabik[0] << tabik[i+1]

tabik[0].save_to_wav("PartioningTest")

plot_aud_array([test, tabik[0]], 'all', True)