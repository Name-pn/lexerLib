class Match():
    def __init__(self, pattern_id, start_index, end_index):
        self.start_index = start_index
        self.end_index = end_index
        self.pattern_id = pattern_id

    def __len__(self):
        return self.end_index - self.start_index