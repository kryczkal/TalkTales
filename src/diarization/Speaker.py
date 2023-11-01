from sklearn.mixture import GaussianMixture
import numpy as np

from ..Settings import Settings


class Speaker:
    """
    Simple class to used to represent different speakers.
    Each speaker has a corresponding GMM model and id
    """

    def __init__(self, id: int):
        """
        Initializes an instance of Speaker class with the id of the speaker
        """
        self.model = GaussianMixture(n_components=16)
        self.training_done = False
        self.id = id

    def model_train(self, mfcc_vectors_array: np.ndarray) -> None:
        """Trains speaker GMM model using provided data"""
        if mfcc_vectors_array.shape[0] >= Settings.MFCC_MAX_SIZE:
            self.training_done = True
            return
        self.model.fit(mfcc_vectors_array)

    def model_get(self):
        """Returns the speaker model for passage into other functions"""
        return self.model


def kl_distance(gmm_x: GaussianMixture, gmm_y: GaussianMixture, n_samples: int = 10 ** 3) -> float:
    """
    Calculates the Kullback-Leibler (KL) divergence between two Gaussian Mixture Models (GMMs), gmm_x and gmm_y.
    
    Args:
        gmm_x (object): Gaussian Mixture Model object \n
        gmm_y (object): Gaussian Mixture Model object \n
        n_samples (int): Number of samples used in comparison
    
    Returns:
        float: KL divergence value
        
    Notes: The function draws n_samples number of samples from the gmm_x using the "sample" method of the GMM object.
    Then, the log-likelihoods of the samples under the two GMMs are calculated using the "score_samples" method of
    both GMMs. The mean of log_prob_y for gmm_x is calculated and then subtracted by the mean of log_prob_y for
    gmm_y. Finally, the KL divergence value is returned. \n
        
        Note that the KL divergence is a measure of how much one probability distribution diverges from another,
        and it is always non-negative. The KL divergence between two GMMs can be used to compare their similarity or
        dissimilarity.
    """
    samples, _ = gmm_x.sample(n_samples)
    log_prob_x = gmm_x.score_samples(samples)
    log_prob_y = gmm_y.score_samples(samples)
    return log_prob_x.mean() - log_prob_y.mean()
