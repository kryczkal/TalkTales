import numpy as np
import matplotlib.pyplot as plt 
from librosa import load
import soundfile as sf
from scipy.signal import spectrogram
from bisect import bisect_left
from help_func import factorize
import soundfile as sf
from scipy.fft import ifft
from copy import deepcopy

SAVE_PATH = ""

class aud:
    def __init__(self, samples, freq = -1):

        if freq == -1:
            self.data, self.freq = sf.read(samples)
            self.__to_mono_array() #obcicie do mono i ustawienie np.array
            self.name = samples
        else:
            self.data = samples
            self.__to_mono_array()
            self.freq = freq

        self.__reset()
    
    def __reset(self):
        self.name = ''
        self.frames = len(self.data)
        self.duration = self.frames / float(self.freq)
        self.time_domain = -1
        self.freq_domain = -1
        self.fourier = -1

    def __plot_name(self, name):
        if self.name != '':
            plt.title(str(name) + " plot of: " + self.name)
        else:
            plt.title("Undefined audio " + str(name) + " plot")
    
    def __to_mono_array(self):
        #Uwaga obcinamy tylko do pierwszego kanalu
        if (type(self.data[0]) == np.ndarray):
            self.data = self.data[:,0]

    def calculate_fourier(self):
        self.fourier = np.fft.fft(self.data)
        self.freq_domain = np.fft.fftfreq(self.frames, 1/self.freq)

        return self.freq_domain, self.fourier
    
    def calculate_time_domain(self):
        self.time_domain = np.linspace(0,self.duration, self.frames)

        return self.time_domain

    def set_name(self, name):
        self.name = str(name)

    def plot(self, type: str = '' ):
        if type == '':
            pass
        elif type == 'db':
            self.setup_db_plot()
        elif type == 'def':
            self.setup_def_plot()
        elif type == 'spect':
            self.setup_spect_plot()
        elif type == 'mel':
            self.setup_mel_plot()
        elif type == 'fourier':
            self.setup_fourier_plot()
        else:
            print("[ERROR]Nie rozpoznano typu wykresu: " + str(type))
        
        plt.show()


    def setup_mel_plot(self):
        1+1

    def setup_fourier_plot(self):
        if type(self.fourier) == int:
            self.calculate_fourier()

        # line = plt.plot(self.freq_domain[:int(self.frames/2)]
        #                 , np.abs(self.fourier[:int(self.frames/2)]))

        line = plt.plot(self.freq_domain, np.real(self.fourier))
        
        plt.xlabel("Czestotliwosc [Hz]")
        plt.ylabel("Amplituda")

        self.__plot_name("Fourier")

        return line

    def setup_def_plot(self):
        if self.time_domain == -1:
            self.calculate_time_domain()


        line = plt.plot(self.time_domain, self.data)
        
        plt.xlabel("Czas [s]")
        plt.ylabel("Amplituda bitowa")

        self.__plot_name("Bit Amplitude")
        
        return line
        
    def setup_db_plot(self, window: float = 0.05):
        #number of arrays to be chopped
        num_of_chunks = int(np.floor(self.duration/float(window)))
        
        #Calculating db value of all windows
        chunks = np.array_split(self.data, num_of_chunks)
        chunks = [20 * np.log10(np.abs(np.mean(chunk))) for chunk in chunks]

        #creating proper time domain
        time = np.linspace(0, self.duration, num_of_chunks)

        line = plt.plot(time, chunks)

        plt.xlabel("Czas [s]")
        plt.ylabel("Amplituda [dB]")

        self.__plot_name("Db Amplitude")
        
        return line
    
    def setup_spect_plot(self, w_size: float = 0.05, overlap: float = -1):
        wind = int (self.freq * w_size)

        if overlap == -1:
            #noverlap = None
            noverlap = 0.025
        else:
            noverlap = int (self.freq * overlap)
        
        freq, time, amp = spectrogram(self.data, fs = self.freq, nperseg = wind, noverlap= noverlap)
        amp = 20 * np.log10(np.abs(amp))

        plt.pcolormesh(time, freq, amp)
        plt.ylabel('Częstotliwość [Hz]')
        plt.xlabel('Czas [s]')


    def split_to_freq_chunks(self, chunks: tuple) -> list:
        if type(chunks) != tuple and type(chunks != tuple):
            raise Exception("Odcinki musza byc podane jako krotka lub lista tzn [x1,x2,x3...], lub w otwartych nawiasach ")

        if type(self.fourier) == int:
            self.calculate_fourier()

        out = []


        if type(chunks[0]) == float or type(chunks[0] == int):
            for i in range(1, len(chunks)):
                keep = np.logical_and(self.freq_domain >= chunks[i-1], self.freq_domain <= chunks[i])
                data = deepcopy(self.fourier)
                data[np.logical_not(keep)] = 0
                out.append(aud(np.real(np.fft.ifft(data)), self.freq))
        elif type(chunks[0]) == list or type(chunks[0]) == tuple:
            for i in range(0, len(chunks)):
                keep = np.logical_and(self.freq_domain >= chunks[i][0], self.freq_domain <= chunks[i][1])
                data = deepcopy(self.fourier)
                data[np.logical_not(keep)] = 0
                out.append(aud(np.real(np.fft.ifft(data)), self.freq))

        if len(out) == 1:
            return out[0]

        return out
    
    def split_to_time_chunks(self, chunks: tuple) -> list:
        if type(chunks) != tuple and type(chunks != tuple):
            raise Exception("Odcinki musza byc podane jako krotka lub lista tzn [x1,x2,x3...], lub w otwartych nawiasach ")

        out = []

        if type(chunks[0]) == float or type(chunks[0] == int):
            for i in range(1, len(chunks)):
                out.append(aud(self.data[chunks[i-1] * self.freq : chunks[i] * self.freq],self.freq))
        elif type(chunks[0]) == list or type(chunks[0]) == tuple:
            for i in range(0, len(chunks)):
                out.append(aud(self.data[chunks[i][0] * self.freq : chunks[i][1] * self.freq],self.freq))

        if len(out) == 1:
            return out[0]

        return out
    
    def split_to_frame_chunks(self, chunks: tuple) -> list:
        ...
        

    def __add__(self, other):
        if (len(self.data) != len(other.data) or self.freq != other.freq):
            raise Exception("Aby dodac tracki musza miec tyle samo probek i ta sama czestotliwosc")
        
        if type(self.fourier) == int:
            self.calculate_fourier()
        
        if type(other.fourier) == int:
            other.calculate_fourier()
        
        
        return aud(np.real(np.fft.ifft(self.fourier + other.fourier)), self.freq)
    

    def __sub__(self, other):
        if (len(self.data) != len(other.data) or self.freq != other.freq):
            raise Exception("Aby odjac tracki musza miec tyle samo probek i ta sama czestotliwosc")
        
        if type(self.fourier) == int:
            self.calculate_fourier()
        
        if type(other.fourier) == int:
            other.calculate_fourier()

        return aud(np.real(np.fft.ifft(self.fourier + other.fourier)), self.freq)
    

    def __mul__(self, other: float):
        if type(other) != int and type(other) != float:
            raise Exception("Stary nie tak sie mnozy: tylko int albo float")
        if type(self.fourier) == int:
            self.calculate_fourier()

        return aud(np.real(np.fft.ifft(self.fourier * other)), self.freq)


    def __rshift__(self, other):
        if type(other) != type(self):
            raise Exception("Halo obudz sie byku, probojesz jakies gowna tu polaczyc")
        if self.freq != other.freq:
            raise Exception("Tracki musza miec ta sama czestotliwosc probkowania aby zsumoawc probki")
        
        other.data = np.concatenate((self.data, other.data))
        other.__reset()

    def __lshift__(self, other):
        if type(other) != type(self):
            raise Exception("Halo obudz sie byku, probojesz jakies gowna tu polaczyc")
        if self.freq != other.freq:
            raise Exception("Tracki musza miec ta sama czestotliwosc probkowania aby zsumoawc probki")
        
        self.data = np.concatenate((self.data, other.data))
        self.__reset()

        
    def save_to_wav(self, name: str = '', path: str = ''):        
        if name == '' and self.name == '':
            name = 'output'
        elif name == '':
            name = self.name

        if path == '':
            path = SAVE_PATH

        sf.write(path + name + '.wav', self.data, self.freq)

    def plot_def(self):
        self.plot('def')

    def plot_spect(self):
        self.plot('spect')

    def plot_db(self):
        self.plot('db')
    
    def plot_fourier(self):
        self.plot('fourier')

    def plot_mel(self):
        self.plot('mel')

def plot_aud_array(input: list[aud], plot_type='def'):
    if plot_type == 'def':
        plocior = aud.setup_def_plot
    elif plot_type == 'db':
        plocior = aud.setup_db_plot
    elif plot_type == 'fourier':
        plocior = aud.setup_fourier_plot
    elif plot_type == 'spect':
        plocior = aud.setup_spect_plot
    else:
        raise Exception("Jedyne dostepne opcje: def, db, fourier, spect")
    
    if len(input) <2:
        raise Exception("Tablica musi miec co najmniej 2 elementy")

    size = factorize(len(input))

    if size[0] == 1:
        size = factorize(len(input)+1)

    for i in range(len(input)):
        plt.subplot(size[0], size[1], i+1)
        plocior(input[i])

    plt.show()


def save_aud_array(input: list[aud],name_list: list[str]= [],path: str = ''):
    if len(input) <2:
        raise Exception("Tablica musi miec co najmniej 2 elementy")
    
    if len(input) > len(name_list):
        for i in range(len(input) - len(name_list)):
            name_list.append('undefined_out_' + str(i))

    for i in range(len(input)):
        input[i].save_to_wav(name_list[i], path)
