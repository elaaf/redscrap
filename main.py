# Main Scrapper File to RUN

# Imports


# Local imports
from redscrap.scrapper import RedScrap
from redscrap.utils import get_command_line_args







if __name__ == "__main__":
    
    # Get command line arguments
    # start_date, end_date, search_terms, subreddits = get_command_line_args()
    
    # Setting parameters
    start_date = "2020-11-01"
    end_date = "2020-11-02"
    
    search_terms = [ "COVID|corona" ]

    
    # Creating a RedScrapper Object
    scrapper = RedScrap(start_date=start_date, 
                        end_date=end_date, 
                        search_terms=search_terms
                        )
    
    # Get Reddit Submissions
    scrapper.retrieve_submissions(retrieve_comments=False)
    