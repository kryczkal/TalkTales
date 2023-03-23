function save_melSpectogram(path, z, folder_path)
%produce spectogram of audio file, z = max frequency
    [y, Fs] = audioread(path);
    windowSize = 2048;
    melSpectrogram(y, Fs, ...
                   'Window',hann(windowSize,'periodic'), ...
                   'OverlapLength',256, ...
                   'FFTLength',2048, ...
                   'NumBands',64, ...s
                   'FrequencyRange',[0,z]);
    out_path = replace(path, ".wav", "_melSpectogram.jpeg");
    [filepath, name, ext] = fileparts(out_path);
    t = replace(name, "_", "-");
    title(t);
    if nargin == 3

        out_path = append(folder_path, name, ext);

    saveas(gcf, out_path);
    
end