class DataLoader:
    """
    Base class for all Data Loaders.
    To add a new topic (e.g., Fishing, Space, History),
    inherit from this class and implement generate().
    """
    def __init__(self):
        self.documents = []
        self.exact_matches = []
        self.related_keywords = []

    def generate(self, count_per_topic=1000):
        """
        Generates data and populates self.documents, self.exact_matches, etc.
        Override this method.
        """
        raise NotImplementedError

    def get_data(self):
        return {
            "documents": self.documents,
            "exact_matches": self.exact_matches,
            "related_keywords": self.related_keywords
        }
