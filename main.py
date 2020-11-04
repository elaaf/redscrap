# Main Scrapper File to RUN

# Imports


# Local imports
from scrapper.pushshift import get_submissions

if __name__ == "__main__":
    
    # Dates to scrape between
    START_DATE = (2020, 1, 1)
    END_DATE =  (2020, 1, 3)
    
    # Search Terms
    search_terms = ["pakistan", "covid"]
    
    # Get Reddit Submissions
    get_submissions(START_DATE, END_DATE, 2, search_query=search_terms)