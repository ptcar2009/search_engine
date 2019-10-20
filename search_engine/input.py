import sys
import os
from typing import List
import glob


def get_file_paths()-> List[str]:
    path_list: List[str] = glob.glob("data/*.txt")

    return path_list
