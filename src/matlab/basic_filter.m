function basic_filter(file_name, low_bar, high_bar, N1, N2)
    [y,Fs]=audioread("data\"+file_name);
    
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


    y_filtered = filter(Lowpass_filter(Fs, high_bar, N2), y);
    y_filtered = filter(Highpass_filter(Fs, low_bar, N1), y_filtered);
    

    udiowrite("data\test\out_"+file_name,y_filtered, Fs);
end
