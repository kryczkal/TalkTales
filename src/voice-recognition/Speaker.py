from sklearn.mixture import GaussianMixture
import numpy as np

class Speaker:
    """
    Simple class to used to represent different speakers. \n
    Each speaker has a corresponding GMM model and id
    """
    def __init__(self, id):
        """
        Initializes an instance of Speaker class with the id of the speaker
        """
        self.model = GaussianMixture(n_components=16)
        #self.data = []
        self.id = id
        

    def model_train(self, data):
        """Trains speaker GMM model using provided data"""
        self.model.fit(data)
    
    def model_get(self):
        """Returns the speaker model for passage into other functions"""
        return self.model
    
    #def data_append(self, sample_data):
    #    self.data = np.append(self.data, sample_data)


def kl_distance_global(gmm_x, gmm_y, n_samples=10 ** 3):
    """
    Calculates the Kullback-Leibler (KL) divergence between two Gaussian Mixture Models (GMMs), gmm_x and gmm_y.
    
    Args:
        gmm_x (object): Gaussian Mixture Model object \n
        gmm_y (object): Gaussian Mixture Model object \n
        n_samples (int): Number of samples to be drawn from the gmm_x GMM 
    
    Returns:
        float: KL divergence value
        
    Notes:
        The function draws n_samples number of samples from the gmm_x using the "sample" method of the GMM object. 
        Then, the log-likelihoods of the samples under the two GMMs are calculated using the "score_samples" method of both GMMs. 
        The mean of log_prob_Y for gmm_x is calculated and then subtracted by the mean of log_prob_Y for gmm_y. 
        Finally, the KL divergence value is returned. \n
        
        Note that the KL divergence is a measure of how much one probability distribution diverges from another, and it is always non-negative. 
        The KL divergence between two GMMs can be used to compare their similarity or dissimilarity.
    """
    samples, _ = gmm_x.sample(n_samples)
    log_prob_X = gmm_x.score_samples(samples)
    log_prob_Y = gmm_y.score_samples(samples)
    return log_prob_X.mean() - log_prob_Y.mean()


def kl_distance_local(gmm_x, gmm_y, samples):
    """
    Calculates the Kullback-Leibler (KL) divergence between two Gaussian Mixture Models (GMMs), gmm_x and gmm_y.
    
    Args:
        gmm_x (object): Gaussian Mixture Model object \n
        gmm_y (object): Gaussian Mixture Model object \n
        sample (2d np array): samples provided to calculate the distance on them 
    
    Returns:
        float: KL divergence value
        
    Notes:
        The function draws n_samples number of samples from the gmm_x using the "sample" method of the GMM object. 
        Then, the log-likelihoods of the samples under the two GMMs are calculated using the "score_samples" method of both GMMs. 
        The mean of log_prob_Y for gmm_x is calculated and then subtracted by the mean of log_prob_Y for gmm_y. 
        Finally, the KL divergence value is returned. \n
        
        Note that the KL divergence is a measure of how much one probability distribution diverges from another, and it is always non-negative. 
        The KL divergence between two GMMs can be used to compare their similarity or dissimilarity.
    """
    log_prob_X = gmm_x.score_samples(samples)
    log_prob_Y = gmm_y.score_samples(samples)
    return log_prob_X.mean() - log_prob_Y.mean()