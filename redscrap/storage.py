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


def gen_save_filename(object, prefix=""):
    subreddits = ",".join(s for s in object.subreddits)
    search_terms = "+".join(q for q in object.search_terms)
    start_date = object.start_epoch
    end_date = object.end_epoch
    
    filename = f"{object.save_path}/{prefix}" + get_sha1(f"{start_date}{end_date}{subreddits}{search_terms}") + ".csv"
    return filename



def save_state(object):
    subreddits = ",".join(s for s in object.subreddits)
    search_terms = "+".join(q for q in object.search_terms)
    start_date = object.start_epoch
    end_date = object.end_epoch
    
    sha1 = get_sha1(f"{start_date}{end_date}{subreddits}{search_terms}")
    
    with open(f"{object.save_path}/{sha1}.state", "wb") as file:
        file.write(str(object.current_start_epoch).encode())
    return


def restore_state(object):
    subreddits = ",".join(s for s in object.subreddits)
    search_terms = "+".join(q for q in object.search_terms)
    start_date = object.start_epoch
    end_date = object.end_epoch
    
    sha1 = get_sha1(f"{start_date}{end_date}{subreddits}{search_terms}")
    
    if os.path.isfile(f"{object.save_path}/{sha1}.state"):
        with open(f"{object.save_path}/{sha1}.state", "rb") as file:
            read_string = file.read()
            object.current_start_epoch = int(read_string.decode())
    
        print("Restored previous state")
        print(f"Resuming from {get_timestamp(object.current_start_epoch)}...")
    return