function saveWave(path, folder_path)
%author: Wojciech Matejuk
%produce wave plot of an audio file
    [y, Fs] = audioread(path);
    out_path = replace(path, ".wav", "_wave.jpeg");
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
    t = (0:length(y)-1)/f;
    plot(t, y);
        
    xlabel('time')
    ylabel('y[n]')
    ylim([-1,1]);
    
    t = replace(name, "_", "-");
    title(t);
    if nargin ==2
        out_path = append(folder_path, name, ext);
    end
    
    saveas(gca, out_path);
end