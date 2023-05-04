from sklearn.mixture import GaussianMixture

class Gmm:
    def __init__(self):
        self.model = GaussianMixture(n_components=16)

    def train(self, data):
        self.model.fit(data)

    def getModel(self):
        return self.model


def gmm_kl(gmm_p, gmm_q, n_samples=10 ** 3):
    X, _ = gmm_p.sample(n_samples)
    log_p_X = gmm_p.score_samples(X)
    log_q_X = gmm_q.score_samples(X)
    return log_p_X.mean() - log_q_X.mean()
