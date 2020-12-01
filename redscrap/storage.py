# Data Management

import os
import csv
import hashlib

# Local Imports
from redscrap.utils import get_timestamp


def get_sha1(string):
    string_sha1 = hashlib.sha1(string.encode())
    return str(string_sha1.hexdigest())

def create_save_dir(save_path):
    # Creating save directory
    if not os.path.exists(save_path):
        os.makedirs(save_path)    
    return


def write_to_csv(DATA_BUFFER, filename):
    keys = DATA_BUFFER[0].keys()
    if os.path.isfile(filename):
        with open(filename, "a", encoding="utf-8") as file:
            writer = csv.DictWriter(file, keys)
            writer.writerows(DATA_BUFFER)
    else:
        with open(filename, "w", encoding="utf-8") as file:
            writer = csv.DictWriter(file, keys)
            writer.writeheader()
            writer.writerows(DATA_BUFFER)
    return