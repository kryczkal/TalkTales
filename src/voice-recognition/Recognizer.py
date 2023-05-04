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
        locmax = self.divergances[-2]
        print(str(locmax))
        if locmax - self.divergances[-1] > 20 and locmax - self.divergances[-3] > 20:
            self.add()
            self.current_speaker = Speaker(max_id)
            max_id+=1
            self.divergances.clear()
            return divergance, 1

        return divergance, 0