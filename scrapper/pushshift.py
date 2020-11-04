# Functions Calling the PushShift API

# Imports
import requests

# Local Imports
from .utils import get_days_diff



##########################################################
#                      For Submissions
##########################################################

def get_submissions(START_DATE, END_DATE, size=1, search_query=[], subreddit=[] , max_retries=1000):
    # API_ENDPOINT = "http://elastic.pushshift.io/reddit/search/submission/?"
    API_ENDPOINT = "http://api.pushshift.io/reddit/search/submission/?"
    
    # Adding result size
    API_ENDPOINT+=f"size={size}"
    
    # Show MetaData
    API_ENDPOINT+=f"&metadata=true"
    
    # Add subreddits to look in
    if subreddit:
        API_ENDPOINT+="&subreddit="
        API_ENDPOINT+=",".join(sub for sub in subreddit)
    
    # Add relevant search queries
    if search_query:
        API_ENDPOINT+="&q="
        API_ENDPOINT+=",".join(q for q in search_query)
    
    
    # Adding between dates
    after, before = get_days_diff(START_DATE, END_DATE)
    
    for day in range(before, after):
        API_ENDPOINT+=f"&after={day}d"
        API_ENDPOINT+=f"&before={day+1}d"
        break    
    print(API_ENDPOINT)
    exit()
    

    return



##########################################################
#                      For Comments
##########################################################

def get_comments(size=1):
    # API_ENDPOINT = "http://elastic.pushshift.io/reddit/search/comment/?"
    API_ENDPOINT = "http://api.pushshift.io/reddit/search/comment/?"
    return
