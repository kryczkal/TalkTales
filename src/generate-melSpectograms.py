#make a spectogram of every audiofile
import matlab.engine
import os
from tqdm import tqdm

eng = matlab.engine.start_matlab()
eng.cd(r'matlab', nargout=0)
data = "../data/"
directory = os.listdir(data)
for file in tqdm(directory):
    eng.saveMelSpectogram("../../data/" + file, 45000, "../../plots/", nargout=0)

