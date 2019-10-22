import sys
import os
from typing import List
import glob
from .inverted_index import inverted_index

def get_file_paths(path: str = "data")-> List[str]:
    path_list: List[str] = glob.glob(f"{path}/*.txt")

    return path_list
