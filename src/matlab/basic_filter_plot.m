function master_fourier(file_name, low_bar, high_bar, N1, N2)
    tiledlayout(2,3)
    [y,Fs]=audioread("data\"+file_name);
    [N,P]=size(y); 
    
    if nargin == 1
        high_bar = 4000;
        low_bar = 100;
        N1 = 100;
        N2 = 100;
    elseif nargin == 2
        high_bar = 4000;
        N1 = 100;
        N2 = 100;
    elseif nargin == 3
        N1 = 100;
        N2 = 100;
    elseif nargin ==4
        N2 = 100;
    end

    function Hd = Lowpass_filter(freq, barrier, strength) 
        h  = fdesign.lowpass('N,F3dB', strength, barrier, freq);
        Hd = design(h, 'butter');
    end

    function Hd = Highpass_filter(freq, barrier, strength)  
        h  = fdesign.highpass('N,F3dB', strength, barrier, freq);
        Hd = design(h, 'butter');
    end

    f=-Fs/2:Fs/(N-1):Fs/2;
    z=fftshift(fft(y)); 

    y_filtered = filter(Lowpass_filter(Fs, high_bar, N2), y);
    y_filtered = filter(Highpass_filter(Fs, low_bar, N1), y_filtered);
    z_filtered = fftshift(fft(y_filtered));
    

    nexttile;
    plot(y)
    title('Przed przerobka')
    xlabel('Czas')
    ylabel('Amplituda')

    nexttile;
    plot(f,abs(z))
    title('Widmo przed odfiltrowaniem wysokich czestotliwosci')
    xlabel('Czestotliwosc');
    ylabel('Amplituda');

    nexttile;
    melSpectrogram(y, Fs, ...
        'OverlapLength',256, ...
        'FFTLength',2880, ...
        'FrequencyRange',[0,Fs/2], ...
        'NumBands',64)
    title('MelSpectrogram przed obrobka')
    xlabel('Czas');
    ylabel('Czestotliwosc');

    nexttile;
    plot(y_filtered)
    title('Po zastosowaniu filtru dolno i gorno przepustowego')
    xlabel('Czas')
    ylabel('Amplituda')

    nexttile;
    plot(f,abs(z_filtered))
    title('Widmo po odfiltrowaniu wysokich czestotliwosci')
    xlabel('Czestotliwosc');
    ylabel('Amplituda');

    nexttile;
    melSpectrogram(y_filtered, Fs, ...
        'OverlapLength',256, ...
        'FFTLength',2880, ...
        'FrequencyRange',[0,Fs/2], ...
        'NumBands',64)
    title('MelSpectrogram po obrobce')
    xlabel('Czas')
    ylabel('Czestotliwosc');
    

    audiowrite("data\test\out_"+file_name,y_filtered, Fs);
end