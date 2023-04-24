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

aud_process.SAVE_PATH = 'Out/'
aud_process.LOAD_PATH = 'In/TODO/'


Sofianame = "44_pokoj_sofia_rode.wav"
Kubaname = "44_pokoj_kuba_rode.wav"
Lukaszname = "44_pokoj_lukasz_rode.wav"
Ernestname = "44_pokoj_ernest_rode.wav"

MateuszName = "44_dworzec_MAteusz_samson.wav"
name = "44_metro_lukasz_samson.wav"

#obj1 = standard_filter(aud(Sofianame))
#obj1 = aud(Sofianame)
obj1 = aud(Kubaname)
#obj1 = standard_filter(aud(Lukaszname))
#obj1 = standard_filter(aud(Ernestname))

obj1 = obj1.split_to_time_chunks((5,10))
#obj1 = aud(lib.effects.trim(obj1.data, top_db=20)[0],obj1.freq)
# obj1.name = Sofianame
# obj1.plot_def()

# obj1.plot_fourier()
# obj1.save_to_wav("f0")
obj1 = standard_filter(obj1)

f0, voiced_flag, voiced_probs = lib.pyin(obj1.data,
                                             fmin=lib.note_to_hz('C1'),
                                             fmax=lib.note_to_hz('C4'))

times = lib.times_like(f0)

D = lib.amplitude_to_db(np.abs(lib.stft(obj1.data)), ref=np.max)
fig, ax = plt.subplots()
img = lib.display.specshow(D, x_axis='time', y_axis='log', ax=ax)
ax.set(title='pYIN fundamental frequency estimation')
fig.colorbar(img, ax=ax, format="%+2.f dB")
ax.plot(times, f0, label='fundamental freq', color='green', linewidth=2)
ax.legend(loc='upper right')

plt.show()