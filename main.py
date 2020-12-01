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
    end_date = "2020-12-01"
    # search_terms_full = [
    #                 "("+
    #                 "Pakistan|Pak|pakistani|paki|پاکستان|لاہور|اسلام آباد"
    #                 +")"
    #                 ,
    #                 "("+
    #                 "covid|corona|covid19|covid-19|coronavirus"
    #                 +"|".join(x for x in ["کرونا", "کورونا", "کورونا وائرس", "corona", "coronavirus","کرونا وائرس","کرونا", "کورونا", "کورونا وائرس", "corona",
    #                 "coronavirus","covid","covid19","covid-19","وائرس", "corona virus",
    #                 "wuhan","ووہان","لاک ڈاؤن","lockdown"])
    #                 +")"
    #                 ]
    
    search_terms = [
                "Pakistan|Pak|pakistani|paki|پاکستان|لاہور"
                ]

    
    # Creating a RedScrapper Object
    scrapper = RedScrap(start_date=start_date, 
                        end_date=end_date, 
                        search_terms=search_terms,
                        buffer_dump_iter=1
                        )
    
    # Get Reddit Submissions
    scrapper.retrieve_submissions(retrieve_comments=True)
    