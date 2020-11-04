# Imports
from datetime import datetime

def get_days_diff(*args):
    """Returns difference between CURRENT DATE and Input dates in format(YEAR, MONTH, DAY)

    Returns:
        tuple: (CurrentDate-InputDate) difference
    """
    out = [(datetime.now()-datetime(*date)).days for date in args]
    return tuple(out)