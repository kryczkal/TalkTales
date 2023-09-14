import numpy as np

from Speaker import Speaker, kl_distance
from Settings import Settings

from SpeakerPlots import SpeakerPlots

class Recongnizer:
    """
    This class implements speaker recognition using KL divergence metric
    """
    def __init__(self, iterations, id, number_treshold = Settings.NUMBER_TRESHOLD, percentage_treshold = Settings.PERCENTAGE_THRESHOLD,
                gmm_is_trained_data_threshold = Settings.GMM_IS_TRAINED_DATA_TRESHOLD):
        """
        Initializes an instance of Recognizer class with default values.
        
        Attributes:
            current_speaker (Speaker): an instance of the Speaker class with an id of 0.
            hypothetical_speaker (Speaker): an instance of the Speaker class with an id of -1.
            speakers (list): a list to keep track of the Speaker instances in the Recognizer class.
            divergences (list): a list to keep track of the Kullback-Liebler (KL) divergence between the current_speaker and hypothetical_speaker.
            max_id (int): the maximum id of the Speaker instances in the Recognizer class.
        """
        self.gmm_is_trained_data_treshold = gmm_is_trained_data_threshold
        self.current_speaker = Speaker(0, gmm_is_trained_data_threshold)
        self.hypothetical_speaker = Speaker(-1, gmm_is_trained_data_threshold)
        self.mfcc_data = None

        # Parameters that set the magnitude of divergence required to consider the current speaker a "new" sp
        self.NUMBER_TRESHOLD = number_treshold # 0
        self.PERCENTAGE_TRESHOLD = percentage_treshold

        self.speakers = []
        self.divergences = [] # TODO: do debugowania: wystarcza dwa
        self.max_id = 1

        self.mfccs_per_append = Settings.SEGMENT_DURATION_MS // 10 # number of mfcc vectors we get from one speech segment 
        self.n_data_per_training = self.mfccs_per_append * iterations # number of mfcc vectors we need to 
        # complete hypothetical speaker training
        
        self.data_in_current_training_iteration = 0 # data currently ammased for the hypothetical speaker
     
        self.has_been_trained_once = False # the first gmm is completely untrained. that leads to errors in compare() fn
        # the following speaker gmms are trained on the data from hypothetical speaker, so the problem exists only with the first speaker
        self.timestamp_counter = 0
        self.id = id
        self.plotter = SpeakerPlots(id)
        

    def save_current_speaker(self):
        """
        Adds the current speaker instance to the list of speakers.
        """
        
        # TODO for gmm in self.speakers:
        self.speakers.append(self.current_speaker)

    def append_data(self, mfcc_vector, error = 0):
        # if the mfcc vector is empty we need to initialize it
        if self.mfcc_data is None:
            self.mfcc_data = mfcc_vector
            return
        
        self.data_in_current_training_iteration += self.mfccs_per_append
        self.mfcc_data = np.append(self.mfcc_data, mfcc_vector, axis=0)
        
        self.timestamp_counter += Settings.SEGMENT_DURATION_MS / 1000 + error

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
        if self.has_been_trained_once and self.if_enough_data():
            divergence = kl_distance(self.current_speaker.model_get(), self.hypothetical_speaker.model_get())
            if Settings.MAKE_PLOTS:
                    self.plotter.add_to_plot(self.current_speaker.id, self.timestamp_counter, divergence)

            #print(f"divergence: {divergence}")
            
            self.divergences.append(divergence)
            if len(self.divergences) < 2:
                return False

            if self.if_speaker_changed():
                if Settings.RECOGNIZER_LOG_SPEAKER_CHANGE:
                    print(f"Speaker change on model {self.id}!")
                self.save_current_speaker()
                self.current_speaker = Speaker(self.max_id, self.gmm_is_trained_data_treshold)
                self.current_speaker.model_train(self.mfcc_data[-self.n_data_per_training:])                 
                self.mfcc_data = self.mfcc_data[-self.n_data_per_training:]

                self.max_id+=1
                print(self.timestamp_counter - Settings.SEGMENT_DURATION_MS / 1000)
                self.divergences.clear()
                return True
            
            

            return False

    def train(self):
        if self.if_enough_data(): 
            self.hypothetical_speaker.model_train(self.mfcc_data[-self.n_data_per_training:])
            if not self.current_speaker.is_trained:
                self.current_speaker.model_train(self.mfcc_data)
            if not self.has_been_trained_once:
                self.has_been_trained_once = True
            return True
        
        return False
    
    def if_enough_data(self):
        return self.data_in_current_training_iteration >= self.n_data_per_training # if we have acumulated data from a interval * 10ms window, we can train the model
    
    def if_speaker_changed(self):
        return self.divergences[-1] - self.divergences[-2] > self.PERCENTAGE_TRESHOLD*self.divergences[-2] \
            and self.divergences[-1] > self.NUMBER_TRESHOLD
    
    def adjust(self):
        if self.if_enough_data():
            self.data_in_current_training_iteration = 0
            # if the speaker is already trained we can delete the mfcc data and gather only enough for the hypothetical speaker to train
            #if self.current_speaker.is_trained:
            #    self.mfcc_data = None

    def plot(self):
        if Settings.MAKE_PLOTS:
            try:
                self.plotter.plot()
            except ZeroDivisionError:
                pass
            print(self)

    def __str__(self) -> str:
        max_width = 25

        messages = [
            ("Recognizer: ", self.id),
            ("SETTINGS: ", None),
            ("Percentage Threshold: ", self.PERCENTAGE_TRESHOLD),
            ("Number Threshold: ", self.NUMBER_TRESHOLD),
            ("Data Threshold: ", self.gmm_is_trained_data_treshold),
        ]
        output = ''
        for message, value in messages:
            formatted_message = message.ljust(max_width)
            if value is not None:
                output += f"\n{formatted_message} {value}"
            else:
                output += f"\n{formatted_message}"
        return output