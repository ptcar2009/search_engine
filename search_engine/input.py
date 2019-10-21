import sys
import os
from typing import List
import glob
from .inverted_index import inverted_index

def get_file_paths()-> List[str]:
    path_list: List[str] = glob.glob("data/*.txt")

    return path_list

if __name__ == "__main__":
    print(inverted_index(get_file_paths()))