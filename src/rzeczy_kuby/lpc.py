from aud_process import aud
from aud_process import save_aud_array
from aud_process import plot_aud_array
from aud_process import read_from_mic
from aud_process import save_plot_aud_array
import aud_process
import os
import librosa as lib
import matplotlib.pyplot as plt
from scipy.signal import lfilter

aud_process.SAVE_PATH = 'Out/'
aud_process.LOAD_PATH = 'In/TODO/'
name = "44_metro_lukasz_samson.wav"

obj1 = aud(name)
obj2 = aud_process.standard_filter(obj1)

filter_b = lib.lpc(obj2.data, order=15)
filter_a = [1.0]
obj5 = aud(lfilter(filter_b, filter_a, obj2.data), obj1.freq)
obj5.save_to_wav("lpc")
