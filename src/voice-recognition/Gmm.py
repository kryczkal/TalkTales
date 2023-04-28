from sklearn.mixture import GaussianMixture as GMM

class Gmm:
    def __init__(self, n_components: int):
        self.model = GMM(n_components=n_components)
