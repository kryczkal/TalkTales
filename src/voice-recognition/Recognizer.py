from Speaker import Speaker, kl_distance

class Recognizer:
    """
    This class implements speaker recognition using KL divergence metric
    """
    def __init__(self):
        """
        Initializes an instance of Recognizer class with default values.
        
        Attributes:
            current_speaker (Speaker): an instance of the Speaker class with an id of 0.
            hypothetical_speaker (Speaker): an instance of the Speaker class with an id of -1.
            speakers (list): a list to keep track of the Speaker instances in the Recognizer class.
            divergances (list): a list to keep track of the Kullback-Liebler (KL) divergence between the current_speaker and hypothetical_speaker.
            max_id (int): the maximum id of the Speaker instances in the Recognizer class.
        """

        self.current_speaker = Speaker(0)
        self.hypothetical_speaker = Speaker(-1)
        self.speakers = []
        self.divergances = []
        self.max_id = 1

    def add(self):
        """
        Adds the current speaker instance to the list of speakers.
        """
        
        # TODO for gmm in self.speakers:
        self.speakers.append(self.current_speaker)

    def compare(self):
        """
        Computes the KL divergence between the current speaker instance and hypothetical speaker instance.
        If the difference in KL divergence is greater than a threshold, and the final KL divergence score is above a certain threshold value, then the current_speaker is added to the speakers list and assigned the next available Speaker id. 
        This method returns the KL divergence value computed and a flag indicating whether or not a new Speaker instance was added to the speaker list.
        
        Returns:
            divergance (float): KL divergence value computed.
            flag (int): Indicates whether or not a new Speaker instance was added to the list of speakers.
                        0: No new Speaker instance was added.
                        1: New Speaker instance was added.
        """

        divergance = kl_distance(self.current_speaker.model_get(), self.hypothetical_speaker.model_get())
        print(f"divergance: {divergance}")
        
        self.divergances.append(divergance)
        if len(self.divergances) < 2:
            return divergance, 0
        if self.divergances[-1] - self.divergances[-2] > 0.35*self.divergances[-2] and self.divergances[-1] > 27:
            self.add()
            self.current_speaker = Speaker(self.max_id)
            self.max_id+=1
            self.divergances.clear()
            return divergance, 1

        return divergance, 0