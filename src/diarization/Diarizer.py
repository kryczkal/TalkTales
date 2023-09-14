import numpy as np

from .Speaker import Speaker, kl_distance
from ..Settings import Settings

from .SpeakerPlots import SpeakerPlots

class Diarizer:
    """
    This class implements speaker diarization using KL divergence metric
    """
    def __init__(self, id: int = 0):
        """
        Initializes an instance of Diarizer class with default values.
        
        Attributes:
            current_speaker (Speaker): an instance of the Speaker class with an id of 0.
            hypothetical_speaker (Speaker): an instance of the Speaker class with an id of -1.
            speakers (list): a list to keep track of the Speaker instances in the Recognizer class.
            divergences (list): a list to keep track of the Kullback-Liebler (KL) divergence between the current_speaker and hypothetical_speaker.
            max_id (int): the maximum id of the Speaker instances in the Recognizer class.
        """
        self.mfcc_vectors_array = None
        # The most important variable, an array of MFCC vectors
        
        self.id = id 
        # id of the diarizer TODO: delete this? Usefull only when running many diarizers at once
        
        # Speaker Models
        self.current_speaker = Speaker(0)
        self.hypothetical_speaker = Speaker(-1)
        
        self.speakers = [] 
        # A list of speaker models for future usage 
        
        self.n_of_speakers = 1 
        # We begin with one speaker
        # TODO: Enable Diarizer to recognize past speakers 

        self.vectors_in_mfcc_array = 0 
        # number of mfcc vectors currently amassed for the hypothetical speaker
        
        # !!! only needed for plotting !!!
        self.elapsed_time_seconds = 0 # We count how long is the Diarizer running (for timestamps) in seconds
        # !!! only needed for plotting !!!

        self.divergences = [] # TODO: wystarcza dwa

        if Settings.MAKE_PLOTS:
            self.plotter = SpeakerPlots(id)

    def save_current_speaker(self):
        """
        Adds the current speaker instance to the list of speakers.
        """
        # TODO for gmm in self.speakers:
        self.speakers.append(self.current_speaker)

    def append_data(self, mfcc_vectors_array: np.ndarray, silent_seconds: int = 0):
        # if the mfcc vector empty is empty we need to initialize it
        if self.mfcc_vectors_array is None:
            self.mfcc_vectors_array = mfcc_vectors_array
            return
        
        self.mfcc_vectors_array = np.append(self.mfcc_vectors_array, mfcc_vectors_array, axis=0)
        self.vectors_in_mfcc_array += Settings.MFCC_PER_SEGMENT

         # We have to make up for the Samples that did not pass VAD test and correct the timer
        self.elapsed_time_seconds += Settings.SEGMENT_DURATION_MS / 1000 + silent_seconds


    def train(self):
        self.hypothetical_speaker.model_train(self.mfcc_vectors_array[-Settings.MFCC_MIN_SIZE:])
        # Uses only MFCC_MIN_SIZE newest mfcc samples to further speakers comparison
        
        if not self.current_speaker.training_done:
            self.current_speaker.model_train(self.mfcc_vectors_array)

    def check_for_speaker_change(self):
        """
        Computes the KL divergence between the current speaker and hypothetical speaker.
        If the difference in KL divergence is greater than a threshold, 
        and the final KL divergence score is above a certain threshold value, 
        then the current_speaker is added to the speakers list and assigned the next available Speaker id. 
        This method returns the KL divergence value computed and a flag indicating whether or not a new Speaker instance was added to the speaker list.
        
        Returns:
            flag (bool): Indicates whether or not a new Speaker instance was added to the list of speakers.
                        False: No new Speaker instance was added.
                        True: New Speaker instance was added.
        """
        divergence = kl_distance(self.current_speaker.model_get(), self.hypothetical_speaker.model_get())
        if Settings.MAKE_PLOTS:
                self.plotter.add_to_plot(self.current_speaker.id, self.elapsed_time_seconds, divergence)
        
        self.divergences.append(divergence)
        if self.if_speaker_changed():
            if Settings.RECOGNIZER_LOG_SPEAKER_CHANGE:
                print(f"Speaker change on model {self.id}!")
                
            self.save_current_speaker()
            self.current_speaker = Speaker(self.n_of_speakers)
            self.current_speaker.model_train(self.mfcc_vectors_array[-Settings.MFCC_MIN_SIZE:])                 
            self.mfcc_vectors_array = self.mfcc_vectors_array[-Settings.MFCC_MIN_SIZE:]
            self.n_of_speakers+=1

            print(self.elapsed_time_seconds - Settings.SEGMENT_DURATION_MS / 1000) # print when was the speaker change
            self.divergences.clear()
            return True
        return False
    
    def if_enough_data(self):
        return self.vectors_in_mfcc_array >= Settings.MFCC_MIN_SIZE

    def if_speaker_changed(self):
        if len(self.divergences) < 2:
            return False
        
        return self.divergences[-1] - self.divergences[-2] > Settings.PERCENTAGE_THRESHOLD*self.divergences[-2] \
            and self.divergences[-1] > Settings.NUMBER_THRESHOLD
    

    def diarize(self, mfcc_vector_array: np.array, silent_seconds: int = 0):
        self.append_data(mfcc_vector_array, silent_seconds)
        if_speaker_changed = False
        if self.if_enough_data():
            self.train()
            if_speaker_changed = self.check_for_speaker_change()
            if self.current_speaker.training_done:
                self.vectors_in_mfcc_array = 0
                self.mfcc_vectors_array = None
        return if_speaker_changed

    def plot(self):
        if Settings.MAKE_PLOTS:
            try:
                self.plotter.plot()
            except ZeroDivisionError:
                pass