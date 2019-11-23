"""
Accessory file for input handling.
"""
import sys
import os
from typing import List
import glob
from .inverted_index import tf_idf_ranking

def get_file_paths(path: str = "data")-> List[str]:
    """
    Gets all file paths in a given directory.

    arguments:
    path - str -> the path from which the files will be gotten
    """
    path_list: List[str] = glob.glob(f"{path}/**/**/*", recursive=True)
    return path_list
