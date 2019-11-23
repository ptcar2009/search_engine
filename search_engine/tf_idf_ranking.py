import os
from typing import Dict, List, Set
from math import log, sqrt
from functools import reduce
import string
import re

class tf_idf_ranking():
    """
    Inverted index is a class that represents the indexes of words relative to documents. 
    """
    _doc_to_words: Dict[str, Dict[str, int]]
    _word_to_docs: Dict[str, Set[str]]

    def __init__(self, documents: List[str] = []):
        """
        Initializes an empty inverted index. 
        """
        self._doc_to_words = {}
        self._word_to_docs = {}
        self.idf_ = {}
        for doc in documents:
            if os.path.isdir(doc):
                continue
            with open(doc) as current:
                formatted_doc = doc.split("/")[-1] # get last part of path
                self._doc_to_words[formatted_doc] = {}
                try:
                    for line in current:
                        for word in line.split():
                            pattern = re.compile('[\W]+') # regex pattern for non wordlike characters
                            word = pattern.sub('',word.lower()) # removing all characters that fit the pattern
                            
                            
                            try:
                                self._doc_to_words[formatted_doc][word] += 1 # if there is an index for the current
                                                                            # word in each document, add one to that index
                            except:
                                self._doc_to_words[formatted_doc][word] = 1 # otherwise, create the given index

                            try:
                                self._word_to_docs[word].add(formatted_doc) # if there is an index for the current document
                                                                            # in each word, add one to that index
                            except:
                                self._word_to_docs[word] = set([formatted_doc])  # otherwise, create given idex
                except:
                    print(doc)
    def __str__(self):
        """Converts the inverted index to a string representation of itself."""
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
        """
        #### Returns the term frequency of a word in a given document or list of words

        Keyword arguments:\n  
        - word: the word of which you want the term frequency
        - doc: the name of the document of which you want to get the frequency of 'word'
        - query: the list of words of a query on which you want the term frequency  
        """

        if doc != None:  # in case there's a document
            try:  # try to get the frequency of words
                return self._doc_to_words[doc][word]

            except:  # if fails, returns 0 as the frequency is non existant
                return 0


        if query == None:  # if there is no query and no document
            raise SyntaxError(  # raise an exception for invalid arguments
                "Invalid call to W. No document and no query given.")

        return sum([1.0 for w in query if w == word]) # count the ammound of occurrences in given query

    def idf(self, word: str) -> float:
        """
        Returns the normalized inverse document frequency of a word, which can be translated to\n
        $$idf(word)=log(\frac{N}{N_{word}})$$

        Where N is the total number of documents and N_word\n 
        is the number of documents on which the word appears on
        """
        try:
            return self.idf_[word]
        except:
            self.idf_[word] = log(
                len(
                    self._doc_to_words
                )
                /
                len(
                    self._word_to_docs[word]
                )
            )

    def W(self, word: str, doc: str = None, query: str = None):
        """
        W is the position of a document or query in relation to the word in question
        """

        if doc != None:
            return self.tf(word=word, doc=doc) * self.idf(word)

        if query == None:
            raise SyntaxError(
                "Invalid call to W. No document and no query given.")

        return self.tf(word=word, query=[w.lower().strip('.?,-! \n') for w in query.split()]) * self.idf(word)

    def sim(self, doc: str, query: str) -> float:
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
        if leftd == 0 or rightd == 0:
            return 0
        return numerator / (leftd * rightd)

    def query(self, query: str, k: int = 10) -> List[str]:
        return sorted(self._doc_to_words.keys(), key=lambda x: self.sim(x, query))[::-1][:k]
