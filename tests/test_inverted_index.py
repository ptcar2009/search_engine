import pytest
from search_engine.inverted_index import inverted_index
import os
import math
import glob


def test_create_new():
    index = inverted_index([os.getcwd() + "/tests/data/test_file_1.txt"])
    assert index, 'Should not be none'
    assert index._doc_to_words == {
        "test_file_1.txt": {"oi": 1, "tudo": 1, "bem": 1}}
    assert index._word_to_docs == {
        "oi": ["test_file_1.txt"],
        "tudo": ["test_file_1.txt"],
        "bem": ["test_file_1.txt"]
    }


def test_tf():
    index = inverted_index()
    index._doc_to_words = {"doc1": {"oi": 5}, "doc2": {}, "doc3": {"oi": 80}}
    assert index.tf("oi", doc="doc1") == 5, 'Should be 5'
    assert index.tf("oi", doc="doc2") == 0, 'Should be 0'
    assert index.tf("oi", doc="doc3") == 80, 'Should be 80'
    assert index.tf("oi", query=["oi"] * 5) == 5, 'Should be 5'
    assert index.tf("oi", query=["oi"] * 80) == 80, 'Should be 80'
    assert index.tf("oi", query=["banana"]) == 0, 'Should be 0'


def test_idf():
    index = inverted_index()
    index._doc_to_words = {"doc1": {"oi": 5}, "doc2": {}, "doc3": {"oi": 80}}
    index._word_to_docs = {"oi": ["doc1", "doc2"]}
    assert index.idf("oi") == math.log(3/2)

def test_W():
    index = inverted_index()
    index._doc_to_words = {"doc1": {"oi": 5}, "doc2": {}, "doc3": {"oi": 80}}
    index._word_to_docs = {"oi": ["doc1", "doc2"]}
    assert index.W("oi", doc="doc1") == math.log(3/2) * 5, 'Should be math.log(3/2) * 5'
    assert index.W("oi", doc="doc2") == 0, 'Should be 0'
    assert index.W("oi", query="doc2") == 0, 'Should be 0'
    assert index.W("oi", doc="doc3") == math.log(3/2) * 80, 'Should be math.log(3/2) * 80'
    assert index.W("oi", query="oi oi oi oi oi") == math.log(3/2) * 5, 'Should be math.log(3/2) * 5'

def test_sim():
    index = inverted_index()
    index._doc_to_words = {"doc1": {"oi": 5}, "doc2": {"boa": 2, "oi": 7}, "doc3": {"oi": 80}}
    index._word_to_docs = {"oi": ["doc1", "doc2"]}
    assert index.sim(doc="doc1", query="oi") == 1
    assert index.sim(doc="doc3", query="oi") == 1
    assert index.sim(doc="doc1", query="boa") == 0


