import numpy as np

from Speaker import Speaker, kl_distance
from Settings import Settings


class Recongnizer:
    """
    This class implements speaker recognition using KL divergence metric
    """
    def __init__(self, iterations, id=0, number_treshold=Settings.NUMBER_TRESHOLD, percentage_treshold=Settings.PERCENTAGE_TRESHOLD,  # noqa: E501
                 gmm_is_trained__data_treshold=Settings.GMM_IS_TRAINED_DATA_TRESHOLD):  # noqa: E501
        """
        Initializes an instance of Recognizer class with default values.

        Attributes:
            current_speaker (Speaker): an instance of the Speaker class with an id of 0.
            hypothetical_speaker (Speaker): an instance of the Speaker class with an id of -1.
            speakers (list): a list to keep track of the Speaker instances in the Recognizer class.
            divergences (list): a list to keep track of the Kullback-Liebler (KL) divergence between the current_speaker and hypothetical_speaker.
            max_id (int): the maximum id of the Speaker instances in the Recognizer class.
        """  # noqa: E501
        self.gmm_is_trained_data_treshold = gmm_is_trained__data_treshold
        self.current_speaker = Speaker(0, gmm_is_trained__data_treshold)
        self.hypothetical_speaker = Speaker(-1, gmm_is_trained__data_treshold)
        self.mfcc_data = None

        self.NUMBER_TRESHOLD = number_treshold  # 0
        self.PERCENTAGE_TRESHOLD = percentage_treshold

        self.speakers = []
        self.divergences = []  # TODO: do debugowania: wystarcza dwa
        self.max_id = 1

        self.mfccs_per_append = Settings.SEGMENT_DURATION_MS // 10
        # number of mfcc vectors we get from one speech segment
        self.n_data_per_hyp_speaker_training = (self.mfccs_per_append
                                                * iterations)
        # number of mfcc vectors we need to
        # complete hypothetical speaker training

        # data currently ammased for the hypothetical speaker
        self.data_in_current_training_iteration = 0

        self.has_been_trained_once = False
        # the first gmm is completely untrained. that leads to errors
        # in the compare() function
        # the following speaker gmms are trained on the data
        # from hypothetical speaker,
        # so the problem exists only with the first speaker
        self.timestamp_counter = 0
        self.id = id

    def save_current_speaker(self):
        """
        Adds the current speaker instance to the list of speakers.
        """

        # TODO for gmm in self.speakers:
        self.speakers.append(self.current_speaker)

    def append_data(self, mfcc_vector, error=0):
        # if the mfcc vector is empty we need to initialize it
        if self.mfcc_data is None:
            self.mfcc_data = mfcc_vector
            return

        self.data_in_current_training_iteration += self.mfccs_per_append
        self.mfcc_data = np.append(self.mfcc_data, mfcc_vector, axis=0)

        self.timestamp_counter += Settings.SEGMENT_DURATION_MS / 1000 + error

    def check_for_speaker_change(self) -> None | float:
        """
        Computes the KL divergence between the current speaker instance and hypothetical speaker instance.
        If the difference in KL divergence is greater than a threshold, and the final KL divergence score is above a certain threshold value, then the current_speaker is added to the speakers list and assigned the next available Speaker id.
        This method returns the KL divergence value computed and a flag indicating whether or not a new Speaker instance was added to the speaker list.

        Returns:
            flag (bool): Indicates whether or not a new Speaker instance was added to the list of speakers.
                        False: No new Speaker instance was added.
                        True: New Speaker instance was added.
        """  # noqa: E501
        if self.has_been_trained_once and self.should_train_and_compare():
            divergence = kl_distance(self.current_speaker.model_get(),
                                     self.hypothetical_speaker.model_get())

            # print(f"divergence: {divergence}")

            self.divergences.append(divergence)
            if len(self.divergences) < 2:
                return None

            if self.crossed_new_speaker_treshold():
                self.save_current_speaker()
                self.current_speaker = Speaker(self.max_id,
                                               self.gmm_is_trained_data_treshold)  # noqa: E501
                self.current_speaker.model_train(self.mfcc_data[-self.n_data_per_hyp_speaker_training:])  # noqa: E501
                self.mfcc_data = self.mfcc_data[-self.n_data_per_hyp_speaker_training:]  # noqa: E501

                self.max_id += 1
                self.divergences.clear()
                return self.timestamp_counter
        return None

    def train(self):
        if self.should_train_and_compare():
            self.hypothetical_speaker.model_train(self.mfcc_data[-self.n_data_per_hyp_speaker_training:])  # noqa: E501
            if not self.current_speaker.is_trained:
                self.current_speaker.model_train(self.mfcc_data)

            self.has_been_trained_once = True
            return True

        return False

    def should_train_and_compare(self):
        # if we have acumulated data from a interval * 10ms window,
        # we can train the model
        return self.data_in_current_training_iteration >= self.n_data_per_hyp_speaker_training  # noqa: E501

    def crossed_new_speaker_treshold(self):
        return (self.divergences[-1] - self.divergences[-2]
                > self.PERCENTAGE_TRESHOLD * self.divergences[-2]
                and self.divergences[-1] > self.NUMBER_TRESHOLD)

    def adjust(self):
        if self.should_train_and_compare():
            self.data_in_current_training_iteration = 0
            # if the speaker is already trained we can delete the mfcc data
            # and gather only enough for the hypothetical speaker to train
            # if self.current_speaker.is_trained:
            #    self.mfcc_data = None

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
