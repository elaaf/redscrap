# Functions Calling the PushShift API

# Imports
import requests
import json
from time import sleep
from tqdm import tqdm
from pprint import pprint

# Local Imports
from redscrap.utils import get_days_diff, get_epoch, get_timestamp, str2tuple, read_jsonfile
from redscrap.storage import create_save_dir, write_to_csv, gen_save_filename



##########################################################
#                      RedScrapper Class
##########################################################

class RedScrap():
    def __init__(self, start_date: str, end_date: str, size: int=1, search_terms: list=[], subreddits :list=[], 
                 max_retries: int=100, max_buffer_size: int=2, friendly_mode: bool=True, friendly_mode_delay: int=0.25):
        self.base_url = {
            "api" : {
                "submissions" : "http://api.pushshift.io/reddit/search/submission/?",
                "comments" : "http://api.pushshift.io/reddit/search/comment/?",
                "comments_for_subid" : "http://api.pushshift.io/reddit/submission/comment_ids/",
                "comments_by_id" : "http://api.pushshift.io/reddit/comment/search?"
            },
            "elastic" : {
                "submissions" : "http://elastic.pushshift.io/reddit/search/submission/?",
                "comments" : "http://elastic.pushshift.io/reddit/search/comment/?"
            }
        }
        self.friendly_mode_toggle = friendly_mode
        self.friendly_mode = {
            True: sleep(friendly_mode_delay),
            False: None
        }
        
        self.max_retries = int(max_retries)
        self.max_buffer_size = int(max_buffer_size)
        self.start_epoch = get_epoch( str2tuple(start_date) )
        self.current_start_epoch = self.start_epoch
        self.end_epoch = get_epoch( str2tuple(end_date) )
        self.size = int(size)
        self.search_terms = search_terms
        self.subreddits = subreddits
        self.config_filename = "./redscrap/config.json"
        self.submission_fields = read_jsonfile(self.config_filename)["submission_fields"]
        self.comment_fields = read_jsonfile(self.config_filename)["comment_fields"]
        self.save_path = f"downloads/{start_date}->{end_date}"
        self.filename_submissions = gen_save_filename( self, prefix="submissions-" )
        self.filename_comments = gen_save_filename( self, prefix="comments-" )
        # Creating Save Directory
        create_save_dir(self.save_path)
        return
    
    
    def __display_config__(self):
        print("================")
        print("=== RedScrap ===")
        print("================")
        print(f"Between: \t\t{get_timestamp(self.start_epoch)} -> {get_timestamp(self.end_epoch)}")
        print(f"Contains (AND): \t{self.search_terms}")
        if not self.subreddits:
            print(f"Search In: \t\tALL SubReddits")
        else:  
            print(f"Search In: \t\t{self.subreddits}")
        print(f"SavePath: \t\t{self.save_path}")
        print("\n")
        return
    
    
    def __get_base_endpoint__(self, access_method: str="api", content_type: str="submissions") -> str:
        # Add metadata and size
        url = f"{self.base_url[access_method][content_type]}"
        # Add fields
        
        if "submission" in content_type:
            url += f"metadata=true&size={self.size}"
            if self.submission_fields:
                fields = ",".join(f for f in self.submission_fields)
                url += f"&fields={fields}"
            # Add search terms
            if self.search_terms:
                search_terms = "+".join(str(x) for x in self.search_terms)
                url += f"&q={search_terms}"
            # Add subreddits
            if self.subreddits:
                subreddits = ",".join(str(x) for x in self.subreddits)
                url += f"&subreddit={subreddits}"
        
        elif "comment" in content_type:
            if self.comment_fields:
                fields = ",".join(f for f in self.comment_fields)
                url += f"fields={fields}"
        return url
    


    def get_request_for_submissions(self, URL):
        response = requests.get(URL)
        status_code = response.status_code
        
        if status_code==200:
            json = response.json()
            metadata = json['metadata']
            data = json['data']
            return status_code, metadata, data
        else:
            return status_code, None, None
    
    
    def retrieve_submissions(self, retrieve_comments=False):
        # STORAGE
        SUBMISSIONS_COUNT, COMMENTS_COUNT = 0, 0
        SUBMISSIONS_BUFFER, COMMENTS_BUFFER = [], []
        
        # Show the current scrapper state
        self.__display_config__()
        
        BASEURL = self.__get_base_endpoint__(access_method="api", content_type="submissions")
        URL = BASEURL+f"&after={self.current_start_epoch}&before={self.end_epoch}"
        # print(f"URL:\n{URL}\n")
        
        # Fetch MetaData
        try:
            _, metadata, _ = self.get_request_for_submissions(URL)
            pbar = tqdm(total=metadata["total_results"], desc="Submissions", leave=False)
            
            
        except Exception as e:
            print("Unable to fetch MetaData")
            print(e)
            exit()
        
        while(True):
            # Requesting
            status_code, retries = 0, -1

            while(status_code!=200 and retries<self.max_retries):
                # Delay to reduce number of requests per second
                self.friendly_mode[self.friendly_mode_toggle]
                
                retries+=1
                status_code, metadata, data = self.get_request_for_submissions(URL)
                total_results = metadata["total_results"]
            
            # Exit scenario - All data scraped
            if total_results==0:
                if SUBMISSIONS_BUFFER:
                    write_to_csv(SUBMISSIONS_BUFFER, self.filename_submissions)
                    SUBMISSIONS_BUFFER.clear()
                if COMMENTS_BUFFER:
                    write_to_csv(COMMENTS_BUFFER, self.filename_comments)
                    COMMENTS_BUFFER.clear()    
                # Exit out the Infinite loop
                break
            
            
            # CONTINUE
            else:
                # Push received submissions into BUFFER
                updt = len(data)
                pbar.update(updt)
                SUBMISSIONS_COUNT += updt
                SUBMISSIONS_BUFFER.extend(data)
                
                # Check if comments are required
                if retrieve_comments:
                    list_of_submission_ids = [ row["id"] for row in data if row["num_comments"]>0 ]
                    # Get all comment ids for 'list_of_submission_ids'
                    list_of_comment_ids = self.retreive_comment_ids_for_submissions(list_of_submission_ids)
                    # Get all comments for 'list_of_comment_ids'
                    comments = self.retrieve_comments_by_id(list_of_comment_ids)
                    
                    # Push received comments into BUFFER
                    COMMENTS_COUNT += len(comments)
                    COMMENTS_BUFFER.extend(comments)
                
                # Get the next batch
                if data:
                    new_start_epoch = data[-1]["created_utc"]
                    self.current_start_epoch = new_start_epoch
                URL = BASEURL+f"&after={self.current_start_epoch}&before={self.end_epoch}"
                
                # Write Data to Disk
                if len(SUBMISSIONS_BUFFER)>=self.max_buffer_size:
                    write_to_csv(SUBMISSIONS_BUFFER, self.filename_submissions)
                    SUBMISSIONS_BUFFER.clear()
                if len(COMMENTS_BUFFER)>=self.max_buffer_size:
                    write_to_csv(COMMENTS_BUFFER, self.filename_comments)
                    COMMENTS_BUFFER.clear()

        pbar.close()
        print("SUCCESS!")
        print(f"Submissions Retreived:\t{SUBMISSIONS_COUNT}")
        print(f"Comments Retreived:\t{COMMENTS_COUNT}")
        return
    
    
    def retreive_comment_ids_for_submissions(self, list_of_submission_ids):
        list_of_comment_ids = []

        URL = self.base_url["api"]["comments_for_subid"]
        for submission_id in tqdm(list_of_submission_ids, desc="Comments", leave=False):
            submission_url = f"{URL}{submission_id}"
            
            
            status_code, retries = 0, -1
            while(status_code!=200 and retries<self.max_retries):
                self.friendly_mode[self.friendly_mode_toggle]
                retries += 1
                response = requests.get(submission_url)
                status_code = response.status_code
                
            retreived_comment_ids = response.json()["data"]
            list_of_comment_ids.extend(retreived_comment_ids)
        
        return list_of_comment_ids
    
    
    def retrieve_comments_by_id(self, list_of_comment_ids):
        URL = self.__get_base_endpoint__(access_method="api", content_type="comments_by_id")
        URL += "&ids=" + ",".join(c for c in list_of_comment_ids)
        
        status_code, retries = 0, -1
        while(status_code!=200 and retries<self.max_retries):
            self.friendly_mode[self.friendly_mode_toggle]
            retries += 1
            response = requests.get(URL)
            status_code = response.status_code

        retreived_comment_ids = response.json()["data"]
        
        return retreived_comment_ids