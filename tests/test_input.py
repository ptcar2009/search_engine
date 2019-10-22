from search_engine.input import get_file_paths

def test_get_file_paths():
    assert get_file_paths("tests/data") == ['tests/data/test_file_1.txt']