function saveMelSpectogram(path, folder_path)
%author: Wojciech Matejuk
%produce spectogram of audio file, z = max frequency
    [y, Fs] = audioread(path);
    out_path = replace(path, ".wav", "_melSpectogram.jpeg");
    windowSize = 2048;
    [~, name, ext] = fileparts(out_path);
    tmp = char(name);
    if(strcmp(tmp(1:2), '22'))
        f = 22050;
    end
    if(strcmp(tmp(1:2), '44'))
        f = 44100;
    end
    if(strcmp(tmp(1:2), '96'))
        f = 96000;
    end

    melSpectrogram(y, Fs, ...
                    'Window',hann(windowSize,'periodic'), ...
                    'OverlapLength',256, ...
                    'FFTLength',2048, ...
                    'FrequencyRange',[0,f/2],...
                    'NumBands',64)
    
    
    t = replace(name, "_", "-");
    title(t);
    if nargin == 2
    
        out_path = append(folder_path, name, ext);
    
    saveas(gca, out_path);
        
    end
end

