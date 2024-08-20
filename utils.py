# utils.py
import re
import os


def clean_filename(filepath):
    """
    Cleans the filename by removing numeric suffixes and file extension.
    :param filepath: str, the path to the file
    :return: str, the cleaned filename without numeric suffixes and extension
    """
    filename = os.path.basename(filepath)
    clean_name = re.sub(r' \(\d+\)|\.\w+$', '', filename)
    return clean_name
