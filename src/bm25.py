import math
from collections import Counter

class BM25:
    """
    Best Matching 25 (BM25) ranking algorithm implemented in pure Python.
    No external libraries (sklearn, numpy) used.
    """
    def __init__(self, corpus, k1=1.5, b=0.75):
        self.k1 = k1
        self.b = b
        self.corpus_size = len(corpus)
        self.avgdl = 0
        self.doc_freqs = []
        self.idf = {}
        self.doc_len = []
        
        self._initialize(corpus)

    def _initialize(self, corpus):
        """
        Calculate IDF and average document length.
        corpus: list of list of strings (tokenized documents)
        """
        total_length = 0
        for doc_tokens in corpus:
            self.doc_len.append(len(doc_tokens))
            total_length += len(doc_tokens)
            
            frequencies = Counter(doc_tokens)
            self.doc_freqs.append(frequencies)
            
            for token in frequencies:
                self.idf[token] = self.idf.get(token, 0) + 1
        
        self.avgdl = total_length / self.corpus_size
        
        # Calculate IDF
        for token, freq in self.idf.items():
            self.idf[token] = math.log(1 + (self.corpus_size - freq + 0.5) / (freq + 0.5))

    def get_score(self, doc_index, query_tokens):
        score = 0.0
        doc_tokens_len = self.doc_len[doc_index]
        frequencies = self.doc_freqs[doc_index]
        
        for token in query_tokens:
            if token not in frequencies:
                continue
                
            freq = frequencies[token]
            numerator = self.idf.get(token, 0) * freq * (self.k1 + 1)
            denominator = freq + self.k1 * (1 - self.b + self.b * doc_tokens_len / self.avgdl)
            score += numerator / denominator
            
        return score

    def get_top_n(self, query_tokens, n=5):
        scores = []
        for index in range(self.corpus_size):
            s = self.get_score(index, query_tokens)
            if s > 0:
                scores.append((index, s))
        
        # Sort by score desc
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:n]
