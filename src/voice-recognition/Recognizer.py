from Speaker import Speaker, kl_distance

class Recognizer:
    def __init__(self):
        self.current_speaker = Speaker(0)
        self.hypothetical_speaker = Speaker(-1)
        self.speakers = []
        self.divergances = []
        self.max_id = 1

    def add(self):
        # TODO for gmm in self.speakers:
        self.speakers.append(self.current_speaker)

    def compare(self):
        divergance = kl_distance(self.current_speaker.model_get(), self.hypothetical_speaker.model_get())
        print(f"divergance: {divergance}")
        
        self.divergances.append(divergance)
        if len(self.divergances) < 2:
            return divergance, 0
        if self.divergances[-1] - self.divergances[-2] > 0.40*self.divergances[-2] and self.divergances[-1] > 30:
            self.add()
            self.current_speaker = Speaker(self.max_id)
            self.max_id+=1
            self.divergances.clear()
            return divergance, 1

        return divergance, 0