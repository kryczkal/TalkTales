import numpy as np
import matplotlib.pyplot as plt 
import soundfile as sf
from scipy.signal import spectrogram
from help_func import factorize
import soundfile as sf
from copy import deepcopy
import pyaudio as pyaud
from librosa.feature import melspectrogram
from librosa import power_to_db
from librosa.display import specshow
import librosa as lib
from scipy.signal import medfilt

SAVE_PATH = ""
LOAD_PATH = ""
PLOT_SAVE_PATH = ""

MULT = 0

class aud:
    def __init__(self, samples, freq = -1):

        if freq == -1:
            self.data, self.freq = sf.read(LOAD_PATH + samples)
            self.__to_mono_array() #obcicie do mono i ustawienie np.array
        else:
            self.data = samples
            self.__to_mono_array()
            self.freq = freq

        self.__reset()
        
        if freq == -1:
            self.name = samples
    
    def __reset(self, name: str = ''):
        self.name = name
        self.frames = len(self.data)
        self.duration = self.frames / float(self.freq)
        self.time_domain = -1
        self.freq_domain = -1
        self.fourier = -1
        self.mel = -1

    def __plot_name(self, name):
        if self.name != '':
            plt.title(str(name) + " plot of: " + str(self.name))
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

    def plot(self, type: str = ''):
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

    def calc_mel(self):
        self.mel = melspectrogram(y=self.data, sr=self.freq)
        return self.mel


    def setup_mel_plot(self, freq_max: int = 10000):
        if type(self.mel) == int:
            self.calc_mel()

        specshow(power_to_db(self.mel, ref=np.max), y_axis='mel', fmax=freq_max, x_axis='time')
        plt.colorbar(format='dB')
        plt.title('Spektrogram MEL')
        plt.tight_layout()
        

    def setup_fourier_plot(self):
        if type(self.fourier) == int:
            self.calculate_fourier()

        line = plt.plot(self.freq_domain[:int(self.frames/2)]
                         , np.abs(self.fourier[:int(self.frames/2)]))

       # line = plt.plot(self.freq_domain, np.real(self.fourier))
        
        plt.xlabel("Czestotliwosc [Hz]")
        plt.ylabel("Amplituda")

        self.__plot_name("Fourier")

        return line

    def change_interval(self, start: int, stop: int):
        if type(start) != int or type(stop) != int:
            raise Exception("Stary przedzial powinnien byc podanym w milisekundac w formacie int")
        elif start > stop:
            raise Exception("Stary juz cie do reszty pojebalo...")
        elif stop > self.duration*1000:
            raise Exception("Przekroczyles zakres nagrania")

        start = int(self.freq * start / 1000)
        stop = int(self.freq * stop / 1000)

        self.data = self.data[start:stop]
        self.__reset(self.name)

    def setup_def_plot(self):
        if type(self.time_domain) == int:
            self.calculate_time_domain()


        line = plt.plot(self.time_domain, self.data)
        
        plt.xlabel("Czas [s]")
        plt.ylabel("Amplituda bitowa")

        self.__plot_name("Bit Amplitude")
        
        return line
        
    def setup_db_plot(self, window: float = 0.05):
        #number of arrays to be chopped
#        num_of_chunks = int(np.floor(self.duration/float(window)))
        
        #Calculating db value of all windows
 #       chunks = np.array_split(self.data, num_of_chunks)
#        chunks = [10 * np.log10(np.abs(np.mean(chunk))) for chunk in chunks]

        #creating proper time domain
        if type(self.time_domain) == int:
            self.calculate_time_domain()

        line = plt.plot(self.time_domain, 20 * np.log10(np.abs(self.data)))

        plt.xlabel("Czas [s]")
        plt.ylabel("Amplituda [dB]")

        self.__plot_name("Db Amplitude")
        
        return line
    
    def setup_spect_plot(self, w_size: float = 0.05, overlap: float = 0.025):
        wind = int (self.freq * w_size)
        noverlap = int (self.freq * overlap)
        
        freq, time, amp = spectrogram(self.data, fs = self.freq, nperseg = wind, noverlap= noverlap)
        amp = 20 * np.log10(np.abs(amp))

        plt.pcolormesh(time, freq, amp)
        plt.ylabel('Częstotliwość [Hz]')
        plt.xlabel('Czas [s]')


    def split_to_freq_chunks(self, chunks: tuple):
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
    
    def split_to_time_chunks(self, chunks: tuple):
        if type(chunks) != tuple and type(chunks) != list:
            raise Exception("Odcinki musza byc podane jako krotka lub lista tzn [x1,x2,x3...], lub w otwartych nawiasach ")

        out = []

        if type(chunks[0]) == float or type(chunks[0] == int):
            for i in range(1, len(chunks)):
                out.append(aud(self.data[int(chunks[i-1] * self.freq) : int (chunks[i] * self.freq)],self.freq))
        elif type(chunks[0]) == list or type(chunks[0]) == tuple:
            for i in range(0, len(chunks)):
                out.append(aud(self.data[int(chunks[i][0] * self.freq) : int(chunks[i][1] * self.freq)],self.freq))

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

        
    def save_to_wav(self, name: str = 'output', path: str = SAVE_PATH):        
        if name == 'output' and self.name != '':
            name = self.name
            sf.write(path + name, self.data, self.freq)
        else:
            sf.write(path + name + '.wav', self.data, self.freq)

    def plot_def(self):
        self.setup_def_plot()
        self.plot()

    def plot_spect(self, w_size: float = 0.05, overlap: float = 0.025):
        self.setup_spect_plot(w_size, overlap)
        self.plot()

    def plot_db(self, window: float = 0.05):
        self.setup_db_plot(window)
        self.plot()
    
    def plot_fourier(self):
        self.setup_fourier_plot()
        self.plot()

    def plot_mel(self, freq_max: int = 10000):
        self.setup_mel_plot(freq_max)
        self.plot()

    def setup_all(self):
        plt.subplot(2,2,1)
        self.setup_def_plot()
        plt.subplot(2,2,2)
        self.setup_fourier_plot()
        plt.subplot(2,2,3)
        self.setup_db_plot()
        plt.subplot(2,2,4)
        self.setup_mel_plot()

    def plot_all(self):
        self.setup_all()
        self.plot()

def plot_aud_array(input: list[aud], plot_type='def', mult_windows = False):
    if plot_type == 'def':
        plocior = aud.setup_def_plot
    elif plot_type == 'db':
        plocior = aud.setup_db_plot
    elif plot_type == 'fourier':
        plocior = aud.setup_fourier_plot
    elif plot_type == 'spect':
        plocior = aud.setup_spect_plot
    elif plot_type == 'all':
        plocior = aud.setup_all
    elif plot_type == 'mel':
        plocior = aud.setup_mel_plot
    else:
        raise Exception("Jedyne dostepne opcje: def, db, fourier, spect, all")
    
    if len(input) <2:
        raise Exception("Tablica musi miec co najmniej 2 elementy")

    if mult_windows == False:
        size = factorize(len(input))

        if size[0] == 1:
            size = factorize(len(input)+1)

        for i in range(len(input)):
            plt.subplot(size[0], size[1], i+1)
            plocior(input[i])
    else:
        for i in range(len(input)):
            plt.figure(i+1)
            plocior(input[i])

    plt.show()

def save_plot_aud_array(input: list[aud], plot_type='def', mult_windows = False):
    if plot_type == 'def':
        plocior = aud.setup_def_plot
    elif plot_type == 'db':
        plocior = aud.setup_db_plot
    elif plot_type == 'fourier':
        plocior = aud.setup_fourier_plot
    elif plot_type == 'spect':
        plocior = aud.setup_spect_plot
    elif plot_type == 'all':
        plocior = aud.setup_all
    else:
        raise Exception("Jedyne dostepne opcje: def, db, fourier, spect, all")
    
    if mult_windows == False:
        size = factorize(len(input))

        if size[0] == 1:
            size = factorize(len(input)+1)

        for i in range(len(input)):
            plt.subplot(size[0], size[1], i+1)
            plocior(input[i])

        plt.savefig(str(MULT) + "GroupPlot.jpg")
    else:
        for i in range(len(input)):
            plocior(input[i])
            plt.savefig(PLOT_SAVE_PATH + str(input[i].name)+ ".jpg")
        plt.close()

def save_aud_array(input: list[aud] , name_list: list[str]= [] , path: str = ''):
    if len(input) <2:
        raise Exception("Tablica musi miec co najmniej 2 elementy")
    
    if len(input) > len(name_list):
        for i in range(len(input) - len(name_list)):
            name_list.append('undefined_out_' + str(i))

    for i in range(len(input)):
        input[i].save_to_wav(name_list[i], path)


def read_from_mic(duration: float = 1000, freq: int = 44100, format = pyaud.paFloat32) -> aud:
    stream = pyaud.PyAudio()
    chunk = int((duration * freq)/1000)
    stream = stream.open(format=format, channels=1, rate=freq, input=True, frames_per_buffer=chunk)

    return aud(np.frombuffer(stream.read(chunk), dtype=np.float32), freq)

def standard_filter(arg: aud) -> aud:
    ret = deepcopy(arg)
    ret = ret.split_to_freq_chunks((100,15000))
    ret = aud(lib.effects.preemphasis(ret.data, coef=0.97), ret.freq)
    ret = ret.split_to_freq_chunks((100,15000))
    ret = aud(lib.util.normalize(ret.data), ret.freq)
    data, _ = lib.effects.trim(ret.data, top_db=20)
    ret = aud(data,ret.freq)
    ret.name = arg.name
    return ret