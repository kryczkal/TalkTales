#make a spectogram of every audiofile
import matlab.engine
eng = matlab.engine.start_matlab()
eng.cd(r'matlab', nargout=0)
eng.saveMelSpectogram("../../data/22_pokoj_wojtek_samson.wav", 25000, "../../plots/", nargout=0)

#do uzupełnienia