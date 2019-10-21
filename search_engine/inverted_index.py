import os
from typing import Dict, List
from math import log, sqrt
from functools import reduce


class inverted_index():
    """
    Inverted index is a class that represents the indexes of words relative to documents. 
    """
    _doc_to_words: Dict[str, Dict[str, int]]
    _word_to_docs: Dict[str, List[str]]

    def __init__(self, documents: List[str] = []):
        """
        Initializes an empty inverted index. 
        """
        self._doc_to_words = {}
        self._word_to_docs = {}

        for doc in documents:
            with open(doc) as current:
                formatted_doc = doc.split("/")[-1]
                self._doc_to_words[formatted_doc] = {}
                for line in current.readlines():
                    for word in line.split():
                        word = word.lower().strip('.?,-! \n')
                        try:
                            self._doc_to_words[formatted_doc][word] += 1
                        except:
                            self._doc_to_words[formatted_doc][word] = 1
                        try:
                            self._word_to_docs[word] += [formatted_doc]
                        except:
                            self._word_to_docs[word] = [formatted_doc]


    def __str__(self):

        formatted: str = ""
        formatted += "Documents:\n"
        for doc in self._doc_to_words.keys():
            formatted += f'\t{doc}:\n'
            for word in self._doc_to_words[doc].keys():
                formatted += f'\t\t{word}: {self._doc_to_words[doc][word]}\n'
        formatted += 'Words:\n'
        for word in self._word_to_docs.keys():
            formatted += f'\t{word}:\n'
            for doc in self._word_to_docs[word]:
                formatted += f'\t\t{doc}\n'

        return formatted

    def tf(self, word: str, doc: str = None, query: List[str] = None) -> float:
        if doc != None:
            try: 
                return self._doc_to_words[doc][word]
            except: 
                return 0
        if query == None:
            raise SyntaxError(
                "Invalid call to W. No document and no query given.")
        return sum([1.0 for w in query if w == word])

    def idf(self, word: str) -> float:
        return log(
            len(self._doc_to_words.keys()) / len(self._word_to_docs[word])
        )

    def W(self, word: str, doc: str = None, query: str = None):
        if doc != None:
            return self.tf(word=word, doc=doc) * self.idf(word)
        if query == None:
            raise SyntaxError(
                "Invalid call to W. No document and no query given.")
        return self.tf(word=word, query=query.split()) * self.idf(word)

    def  sim(self, doc: str, query: str) -> float:
        numerator: float = sum([
            self.W(word=w, doc=doc) *
            self.W(word=w, query=query)
            for w in self._word_to_docs.keys()]
        )
        leftd: float = sqrt(sum([
            self.W(word=w, doc=doc) ** 2
            for w in self._word_to_docs.keys()
        ]))
        rightd: float = sqrt(sum([
            self.W(word=w, query=query) ** 2
            for w in self._word_to_docs.keys()
        ]))
        if leftd == 0 or rightd == 0: return 0
        return numerator / (leftd * rightd)

    def query(self, query: str, k: int = 10) -> List[str]:
        return sorted(map(lambda x: self.sim(x, query), self._doc_to_words.keys()))[:k]