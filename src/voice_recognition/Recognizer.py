import numpy as np

from Speaker import Speaker, kl_distance
from Settings import Settings
class Recongnizer:
    """
    This class implements speaker recognition using KL divergence metric
    """
    def __init__(self, iterations):
        """
        Initializes an instance of Recognizer class with default values.
        
        Attributes:
            current_speaker (Speaker): an instance of the Speaker class with an id of 0.
            hypothetical_speaker (Speaker): an instance of the Speaker class with an id of -1.
            speakers (list): a list to keep track of the Speaker instances in the Recognizer class.
            divergences (list): a list to keep track of the Kullback-Liebler (KL) divergence between the current_speaker and hypothetical_speaker.
            max_id (int): the maximum id of the Speaker instances in the Recognizer class.
        """

        self.current_speaker = Speaker(0)
        self.hypothetical_speaker = Speaker(-1)
        self.mfcc_data = None

        self.NUMBER_TRESHOLD = 40
        self.PERCENTAGE_TRESHOLD = 0.50

        self.speakers = []
        self.divergences = [] # Todo: do debugowania: wystarcza dwa
        self.max_id = 1

        self.mfccs_per_append = Settings.SEGMENT_DURATION_MS // 10
        self.data_number_treshold = self.mfccs_per_append * iterations

        self.data_counter = 0

        self.is_trained = False

    def save_current_speaker(self):
        """
        Adds the current speaker instance to the list of speakers.
        """
        
        # TODO for gmm in self.speakers:
        self.speakers.append(self.current_speaker)

    def append_data(self, mfcc_vector):
        if self.mfcc_data is None:
            self.mfcc_data = mfcc_vector
            return
            
        self.data_counter += self.mfccs_per_append
        self.mfcc_data = np.append(self.mfcc_data, mfcc_vector, axis=0)

    def check_for_speaker_change(self):
        """
        Computes the KL divergence between the current speaker instance and hypothetical speaker instance.
        If the difference in KL divergence is greater than a threshold, and the final KL divergence score is above a certain threshold value, then the current_speaker is added to the speakers list and assigned the next available Speaker id. 
        This method returns the KL divergence value computed and a flag indicating whether or not a new Speaker instance was added to the speaker list.
        
        Returns:
            flag (bool): Indicates whether or not a new Speaker instance was added to the list of speakers.
                        False: No new Speaker instance was added.
                        True: New Speaker instance was added.
        """
        if not self.is_trained or not self.should_train_and_compare():
            return False

        divergence = kl_distance(self.current_speaker.model_get(), self.hypothetical_speaker.model_get())
        print(f"divergence: {divergence}")
            
        self.divergences.append(divergence)
        if len(self.divergences) < 2:
            return False
        if self.crossed_new_speaker_treshold():
                
            self.save_current_speaker()
            self.current_speaker = Speaker(self.max_id)
            self.current_speaker.model_train(self.mfcc_data[-self.data_number_treshold:])

            self.mfcc_data = self.mfcc_data[-self.data_number_treshold:]

            self.max_id+=1
            self.divergences.clear()
            return True

        return False

    def train(self):
        if not self.should_train_and_compare():
            return False

        self.hypothetical_speaker.model_train(self.mfcc_data[-self.data_number_treshold:])
        self.current_speaker.model_train(self.mfcc_data)
        self.is_trained = True
        return True
        

    def should_train_and_compare(self):
        return self.data_counter >= self.data_number_treshold # if we have acumulated data from a interval * 10ms window, we can train the model

    def crossed_new_speaker_treshold(self):
        return self.divergences[-1] - self.divergences[-2] > self.PERCENTAGE_TRESHOLD*self.divergences[-2] \
            and self.divergences[-1] > self.NUMBER_TRESHOLD
    
    def adjust(self):
        if self.should_train_and_compare():
            self.data_counter = 0