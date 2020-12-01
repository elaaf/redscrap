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


def gen_save_filename(object):
    subs = ",".join(s for s in object.subreddits)
    query = "+".join(q for q in object.search_terms)
    start_date = get_timestamp( object.start_epoch )
    end_date = get_timestamp( object.end_epoch )
    
    filename = f"{object.save_path}/" + get_sha1(f"{start_date}--{end_date}--sub={subs}--query={query}") +".csv"
    return filename