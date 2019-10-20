from typing import Dict, List
class inverted_index():
    """
    Inverted index is a class that represents the indexes of words relative to documents. 
    """
    _doc_to_words : Dict[str, Dict[str, int]]
    _word_to_docs : Dict[str, Dict[str, int]]
    
    def __init__(self, documents : List[str] = []):
        """
        Initializes an empty inverted index. 
        """
        self._doc_to_words = {}
        self._word_to_docs = {}
    
    def get_words(self, doc : str) -> List[str]:
        return self._doc_to_words[doc]

    def get_docs(self, word : str) -> List[str]:
        return self._word_to_docs[word]
