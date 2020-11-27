# Functions Calling the PushShift API

# Imports
import requests
import json
from time import sleep
from tqdm import tqdm
from pprint import pprint

# Local Imports
from redscrap.utils import get_days_diff, get_epoch, get_timestamp, str2tuple, read_jsonfile
from redscrap.storage import create_save_dir, write_to_csv



##########################################################
#                      RedScrapper Class
##########################################################

class RedScrap():
    def __init__(self, start_date: str, end_date: str, size: int=1, 
                 search_terms: list=[], subreddits :list=[], 
                 fields: list=[],
                 max_retries: int=100,
                 max_buffer_size: int=2, friendly_mode_delay: int=0.75):
        self.base_url = {
            "api" : {
                "submissions" : "http://api.pushshift.io/reddit/search/submission/?",
                "comments" : "http://api.pushshift.io/reddit/search/comment/?"
            },
            "elastic" : {
                "submissions" : "http://elastic.pushshift.io/reddit/search/submission/?",
                "comments" : "http://elastic.pushshift.io/reddit/search/comment/?"
            }
        }
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
        self.fields = read_jsonfile(self.config_filename)["fields"]
        self.save_path="downloads"
        self.filename = self.__gen_filename__(start_date, end_date)
        self.base_end_point = self.__get_base_endpoint__(access_method="api", content_type="submissions")
        # Creating Save Directory
        create_save_dir(self.save_path)
        return
    
    def __display_config__(self):
        print("================")
        print("=== RedScrap ===")
        print("================")
        print(f"Between: \t\t{get_timestamp(self.start_epoch)}->{get_timestamp(self.end_epoch)}")
        print(f"Contains (AND): \t{self.search_terms}")
        if not self.subreddits:
            print(f"Search In: \t\tALL SubReddits")
        else:  
            print(f"Search In: \t\t{self.subreddits}")
        print("\n")
        return
    
    
    def __gen_filename__(self, start_date, end_date):
        subs = ",".join(s for s in self.subreddits)
        query = "+".join(q for q in self.search_terms)
        filename = f"{self.save_path}/{start_date}--{end_date}--sub={subs}--query={query}.csv"
        return filename
    
    
    def __get_base_endpoint__(self, access_method: str="api", content_type: str="submissions") -> str:
        # Add metadata and size
        url = f"{self.base_url[access_method][content_type]}metadata=true&size={self.size}"
        # Add fields
        if self.fields:
            fields = ",".join(f for f in self.fields)
            url += f"&fields={fields}"
        # Add search terms
        if self.search_terms:
            search_terms = "+".join(str(x) for x in self.search_terms)
            url += f"&q={search_terms}"
        # Add subreddits
        if self.subreddits:
            subreddits = ",".join(str(x) for x in self.subreddits)
            url += f"&subreddit={subreddits}"
        return url
    
    
    def __get_endpoint__(self) -> str:
        # Add before and after dates
        url = f"{self.base_end_point}&after={self.current_start_epoch}&before={self.end_epoch}"
        return url


    def get_request(self, URL):
        response = requests.get(URL)
        status_code = response.status_code
        
        if status_code==200:
            json = response.json()
            metadata = json['metadata']
            data = json['data']
            return status_code, metadata, data
        else:
            return status_code, None, None
    
    
    def retrieve_submissions(self, friendly_mode=True):
        
        # Show the current scrapper state
        self.__display_config__()
        
        DATA_BUFFER = []
        URL = self.__get_endpoint__()
        # print(f"URL:\n{URL}\n")
        
        # Fetch MetaData
        try:
            _, metadata, _ = self.get_request(URL)
            pbar = tqdm(total=metadata["total_results"])

        except Exception as e:
            print("Unable to fetch MetaData")
            print(e)
            exit()
        
        while(True):
            # Requesting
            status_code = 0
            retries = -1

            while(status_code!=200 and retries<self.max_retries):
                # Delay to reduce number of requests per second
                self.friendly_mode[friendly_mode]
                
                retries+=1
                status_code, metadata, data = self.get_request(URL)
                total_results = metadata["total_results"]
            
            if total_results==0:
                if DATA_BUFFER:
                    write_to_csv(DATA_BUFFER, self.filename)
                break
            else:
                # Push received data into BUFFER
                pbar.update(len(data))
                DATA_BUFFER.extend(data)
            
                # Get the next batch
                if data:
                    new_start_epoch = data[-1]["created_utc"]
                    self.current_start_epoch = new_start_epoch
                URL = self.__get_endpoint__()
                
                # Write Data to Disk
                if len(DATA_BUFFER)>=self.max_buffer_size:
                    write_to_csv(DATA_BUFFER, self.filename)
                    DATA_BUFFER.clear()

        pbar.close()
        return