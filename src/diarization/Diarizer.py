import numpy as np
import copy

from .Speaker import Speaker, kl_distance
from ..Settings import Settings
from .Sample import VoiceSample

from .SpeakerPlots import SpeakerPlots


class Diarizer:
    """
    The Diarizer class processes and analyzes speech samples to detect and identify different 
    speakers in a conversation. It examines the MFCC vectors of the speech samples and measures 
    the divergence between the current and hypothetical speaker models.
    """

    def __init__(self, id: int = 0):
        """
        Constructor for initializing the Diarizer object.
        """
        self.mfcc_vectors_array = None
        # The most important variable, an array of MFCC vectors

        self.id = id
        # id of the diarizer TODO: delete this? Useful only when running many diarizers at once

        # Speaker Models
        self.current_speaker = Speaker(0)
        self.hypothetical_speaker = Speaker(1)

        self.speakers = []
        # A list of speaker models for future usage 

        self.n_of_speakers = 1
        # We begin with one speaker
        # TODO: Enable Diarizer to recognize past speakers 

        self.vectors_in_mfcc_array = 0
        # number of mfcc vectors currently amassed for the hypothetical speaker

        # !!! only needed for plotting !!!
        self.elapsed_time_seconds = 0  # We count how long is the Diarizer running (for timestamps) in seconds
        # !!! only needed for plotting !!!

        self.divergences = []  # TODO: two of them are enough

        self.test_delay_counter = 0  # Counts the progress towards SETTINGS.TEST_DELAY_IN_MS

        if Settings.MAKE_PLOTS:
            self.plotter = SpeakerPlots(id)

    def save_current_speaker(self) -> None:
        """
        Adds the current speaker instance to the list of speakers.
        """
        # TODO for gmm in self.speakers:
        self.speakers.append(self.current_speaker)

    def append_data(self, mfcc_vectors_array: np.ndarray, silent_seconds: int = 0) -> None:
        """
        Appends MFCC vectors to the mfcc_vectors_array. 
        Corrects the timer to account for segments that didn't pass the VAD test.
        """
        # if the mfcc vector empty is empty we need to initialize it
        if self.mfcc_vectors_array is None:
            self.mfcc_vectors_array = mfcc_vectors_array
            return

        self.mfcc_vectors_array = np.append(self.mfcc_vectors_array, mfcc_vectors_array, axis=0)
        self.vectors_in_mfcc_array += Settings.MFCC_PER_SEGMENT

        # We have to make up for the Samples that did not pass VAD test and correct the timer
        self.elapsed_time_seconds += Settings.SEGMENT_DURATION_S + silent_seconds

    def train(self) -> None:
        """
        Trains the models for the current and hypothetical speakers.
        """
        self.hypothetical_speaker.model_train(self.mfcc_vectors_array[-Settings.MFCC_MIN_SIZE:])
        # Uses only MFCC_MIN_SIZE newest mfcc samples to further speakers comparison

        if not self.current_speaker.training_done:
            self.current_speaker.model_train(self.mfcc_vectors_array)

    def check_for_speaker_change(self) -> bool:
        """
        Computes the KL divergence between the current speaker and hypothetical speaker.
        If the difference in KL divergence is greater than a threshold, 
        and the final KL divergence score is above a certain threshold value, 
        then the current_speaker is added to the speakers list and assigned the next available Speaker id. 
        This method returns a flag indicating whether a new Speaker instance was added to the speaker list.
        
        Returns:
            flag (bool): Indicates whether a new Speaker instance was added to the list of speakers.
                        False: No new Speaker instance was added.
                        True: New Speaker instance was added.
        """

        divergence = kl_distance(self.current_speaker.model_get(), self.hypothetical_speaker.model_get())
        self.divergences.append(divergence)

        if Settings.MAKE_PLOTS:
            self.plotter.add_to_plot(self.current_speaker.id, self.elapsed_time_seconds, divergence)
        if self.if_speaker_changed():
            if Settings.RECOGNIZER_LOG_SPEAKER_CHANGE:
                print(f"Speaker change on model {self.id}! divergence {self.divergences[-1]}")

            self.save_current_speaker()
            self.current_speaker = self.hypothetical_speaker
            self.n_of_speakers += 1
            self.hypothetical_speaker = Speaker(self.n_of_speakers)
            self.mfcc_vectors_array = self.mfcc_vectors_array[-Settings.MFCC_MIN_SIZE:]
            self.vectors_in_mfcc_array = Settings.MFCC_MIN_SIZE

            print(self.elapsed_time_seconds - Settings.SEGMENT_DURATION_S)  # print when was the speaker change
            self.divergences.clear()
            return True

        # if no changes 
        return False

    def if_enough_data(self) -> bool:
        """
        Checks if there's sufficient data (MFCC vectors) to proceed with training or comparisons.
        """
        return self.vectors_in_mfcc_array >= Settings.MFCC_MIN_SIZE

    def if_speaker_changed(self) -> bool:
        """
        Compares the most recent divergence values to determine if there has been a significant change in speakers.
        """
        if len(self.divergences) < 2:
            return False

        return self.divergences[-1] - self.divergences[-2] > Settings.PERCENTAGE_THRESHOLD * self.divergences[-2] \
            and self.divergences[-1] > Settings.NUMBER_THRESHOLD

    def diarize(self, byte_data: bytes) -> bool:
        """
        Main method to process a given voice sample. 
        Converts the byte data into MFCC vectors and checks for potential speaker changes at regular intervals. 
        Returns a flag if a new speaker has been detected.
        """

        sample = VoiceSample(copy.copy(byte_data))
        # Returns if passed byte data is not valid
        if not sample.if_is_speech():
            return False

        self.append_data(sample.mfcc_get().T, VoiceSample.silent_seconds)
        # We check for speaker changes every SETTINGS.TEST_DELAY_IN_MS
        if self.test_delay_counter < Settings.TEST_DELAY_IN_MS:
            self.test_delay_counter += Settings.SEGMENT_DURATION_MS
            return False
        else:
            # We need at least SETTINGS.MFCC_MIN_SIZE mfcc vectors to train the model for reliable results
            if self.if_enough_data():
                self.test_delay_counter = 0
                # We only need to train the model before check_for_speaker_change()
                # Not for example every 10ms
                self.train()
                if_speaker_changed = self.check_for_speaker_change()  # <- this should be not working properly,
                # since it needs two different divergences to work

                # If the model is trained we cease training him,
                # and only need vectors for hypothetical speaker (SETTINGS.MFCC_MIN_SIZE)

                if self.current_speaker.training_done:
                    self.vectors_in_mfcc_array = 0
                    self.mfcc_vectors_array = None
                return if_speaker_changed
            return False

    def plot(self):
        """
        Plots the speaker data if the settings allow for plotting.
        """
        if Settings.MAKE_PLOTS:
            try:
                self.plotter.plot()
            except ZeroDivisionError:
                pass
