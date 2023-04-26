import numpy as np
from sklearn.mixture import GaussianMixture as GMM


class Speaker:

    def __init__(self, name, model):
        self.name = name
        self.model = model


class RecognizerGMM:

    def __init__(self, n_components=16):
        self.n_components = n_components
        self.speakers = []


    def enroll(self, name, data):
        gmm = GMM(n_components=self.n_components).fit(data)
        self.speakers.append(Speaker(name, gmm))

    def predict(self, data):
        scores = []
        for speaker in self.speakers:
            scores.append((speaker.name, speaker.model.score(data)))
        return sorted(scores, key=lambda x:x[1], reverse=True)
