from sklearn.mixture import GaussianMixture
from pycave.bayes import GaussianMixture as pyCaveMixture
class GMM:
    def __init__(self, Data):
        self.model = GaussianMixture(n_components=1)
        self.pymodel = pyCaveMixture(1)
        self.model.fit(Data)
        self.pymodel.fit(Data)
    def Train(self, Data, components):
        self.model.fit(Data)
    def pyTrain(self, Data):
        self.pymodel.fit(Data)