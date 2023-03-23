# make a spectogram of every audio file
import matlab.engine
import os
from tqdm import tqdm

eng = matlab.engine.start_matlab()
eng.cd(r'matlab', nargout=0)
data = "../data/"
directory = os.listdir(data)
for file in tqdm(directory):
    try:
        eng.saveMelSpectogram("../../data/" + file,
                              "../../plots/melSpectograms/", nargout=0)
    finally:
        continue
