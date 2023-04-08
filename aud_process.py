import numpy as np
import matplotlib.pyplot as plt 
from librosa import load
from scipy.signal import spectrogram
from bisect import bisect_left
from help_func import factorize
import soundfile as sf


SAVE_PATH = ""

class aud:
    def __init__(self, samples, freq = -1):

        if freq == -1:
            self.data, self.freq = load(samples)
            self.data = np.array(self.data)
            self.name = samples
        else:
            self.data = np.array(samples)
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


    def calculate_fourier(self):
        self.fourier = np.fft.fft(self.data)
        self.freq_domain = np.fft.fftfreq(self.frames, 1/self.freq)

        return self.freq_domain, self.fourier
    
    def calculate_time_domain(self):
        self.time_domain = np.linspace(0,self.duration, self.frames)

        return self.time_domain

    def set_name(self, name):
        self.name = str(name)

    def plot(self):
        plt.show()


    def setup_plot_fourier(self):
        if self.fourier == -1:
            self.calculate_fourier()

        line = plt.plot(self.freq_domain[:int(self.frames/2)]
                        , np.abs(self.fourier[:int(self.frames/2)]))
        
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
        
    def setup_db_plot(self, window = 0.05):
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
    
    def setup_spect_plot(self, w_size = 0.05, overlap = 0.025):
        wind = int (self.freq * w_size)
        noverlap = int (self.freq * overlap)
        
        freq, time, amp = spectrogram(self.data, fs = self.freq, nperseg = wind, noverlap= noverlap)
        amp = 20 * np.log10(np.abs(amp))

        plt.pcolormesh(time, freq, amp)
        plt.ylabel('Częstotliwość [Hz]')
        plt.xlabel('Czas [s]')


    def split_to_chunks(self, chunks):
        if self.fourier == -1:
            self.calculate_fourier()

        out = []
        freq = list(self.freq_domain)
        freq = freq[:int(self.frames/2)]
        start = bisect_left(freq, float(chunks[0]))

        for i in range(1, len(chunks)):
            stop = bisect_left(freq, float(chunks[i]))
            data = np.fft.ifft(np.pad(self.fourier[start:stop], (start, self.frames-stop)))
            out.append(aud(data, self.freq))
            start = stop
            #print(len(out[i-1].data))
        
        return out

    def __add__(self, other):
        if (len(self.data) != len(other.data) or self.freq != other.freq):
            raise Exception("Aby dodac tracki musza miec tyle samo probek i ta sama czestotliwosc")
        
        if self.fourier == -1:
            self.calculate_fourier()
        
        if other.fourier == -1:
            other.calculate_fourier()
        
        
        return aud(np.fft.ifft(self.fourier + other.fourier), self.freq)
    

    def __sub__(self, other):
        if (len(self.data) != len(other.data) or self.freq != other.freq):
            raise Exception("Aby odjac tracki musza miec tyle samo probek i ta sama czestotliwosc")
        
        if self.fourier == -1:
            self.calculate_fourier()
        
        if other.fourier == -1:
            other.calculate_fourier()

        return aud(np.fft.ifft(self.fourier + other.fourier), self.freq)
    

    def __mul__(self, other: float):
        if self.fourier == -1:
            self.calculate_fourier()

        return aud(np.ifft(self.fourier * other), self.freq)


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

        
    def save_to_wav(self, path: str = '', name: str = ''):        
        if name == '' and self.name == '':
            name = 'output'
        elif name == '':
            name = self.name

        if path == '':
            path = SAVE_PATH

        sf.write(path + name + '.wav', self.data, self.freq)
    

def plot_aud_array(input: list[aud], plot_type='def'):
    if plot_type == 'def':
        plocior = aud.setup_def_plot
    elif plot_type == 'db':
        plocior = aud.setup_db_plot
    elif plot_type == 'fourier':
        plocior = aud.setup_plot_fourier
    elif plot_type == 'spect':
        plocior = aud.setup_spect_plot
    else:
        raise Exception("Jedyne dostepne opcje: def, db, fourier, spect")
    
    if len(input) <2:
        raise Exception("Tablica musi miec co najmniej 2 elementy")

    size = factorize(len(input))

    for i in range(len(input)):
        plt.subplot(size[0], size[1], i+1)
        plocior(input[i])

    plt.show()


def save_aud_array(input: list[aud],path: str = '' ,name_list: list[str]= []):
    if len(input) <2:
        raise Exception("Tablica musi miec co najmniej 2 elementy")
    
    if len(input) > len(name_list):
        for i in range(len(input) - len(name_list)):
            name_list.append('undefined_out_' + str(i))

    for i in range(len(input)):
        input[i].save_to_wav(path, name_list[i])
    