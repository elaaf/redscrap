# Imports
import os
import json
import argparse
from datetime import datetime, timedelta



def read_jsonfile(filename):

    if os.path.isfile(filename):
        with open(filename, "r") as f:
            config = json.load(f)
            return config
    else:
        print(f"ERROR: {filename} Not Found!")
        return None


def get_epoch(input_date: tuple) -> int:
    """Returns unix epochs value for date tuple of 
    format (Year,Month,Day,Hour,Min,Sec).

    Args:
        input_date (tuple): DateTime (Year,Month,Day,Hour,Min,Sec)

    Returns:
        int: Unix epoch value
    """
    return int(datetime(*tuple(input_date)).timestamp())


def get_timestamp(epoch: int) -> str:
    """Returns timestamp for a unix epochs value.
    
    Args:
        epoch (int): Unix epoch
    
    Returns:
        string: Timestamp
    """
    return datetime.fromtimestamp(epoch).strftime('%Y-%m-%d')


def get_days_diff(input_date: tuple) -> int:
    """Returns days difference between CURRENT DATETIME and 
    Input date of format (Year,Month,Day,Hour,Min,Sec).
    
    Returns:
        int: (CurrentDate-InputDate) difference
    """
    return (datetime.now()-datetime(*input_date)).days


def str2tuple(string: str, sep: str="-") -> tuple:
    """Converts string to a tuple of int based on a separator character.

    Args:
        string (str): String to convert
        sep (str, optional): Charactor to split string on. Defaults to "-".

    Returns:
        tuple: A tuple of ints, from parsed string
    """
    return tuple([int(x) for x in string.split(sep)])


def get_command_line_args():
    """Parses command line arguments.

    Returns:
        Namespace obj: A Namespace objects (similar to a named tuple)
    """
    parser = argparse.ArgumentParser(description="Requires Scrapper Arguements")
    
    parser.add_argument("-s", "--start", dest="start_date",
                        default=(datetime.now()+timedelta(days=-10)).strftime("%Y-%m-%d") )
    parser.add_argument("-e", "--end", dest="end_date",
                        default=datetime.now().strftime("%Y-%m-%d") )
    parser.add_argument("-q", "--search_terms", dest="search_terms", type=str,
                        nargs="*", default=[])
    parser.add_argument("-sub", "--subreddits", dest="subreddits", type=str,
                        nargs="*", default=[])
    args = parser.parse_args()
    
    return args.start_date, args.end_date, args.search_terms, args.subreddits