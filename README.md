# RedScrap
A Reddit Scrapper built around the [PushShift API](https://github.com/pushshift/api "PushShift API").

![RedScrap](http://github.com/elaaf/redscrap/images/usage.png)


## Features

* Get old Reddit submissions (and their comments)
* Save to CSV files for easy loading/usage
* Complex Search Query support and sepcify Subreddits to restrict search
* Resume from last saved state

![Resume State](http://github.com/elaaf/redscrap/images/resume.png)

## Requirements
```bash
# Create a Python 3.6+ virtual environment and run
pip install -r requirements.txt
```

## How To Run This Code

Clone this repo.
```bash
git clone https://github.com/elaaf/redscrap.git
```

## Usage

Either import the RedScrap class OR alter and run main.py

#### The RedScrap Class

```python
from redscrap.scrapper import RedScrap
```

```python
# Search between dates...
start_date = "2020-10-01"
end_date = "2020-10-02"

# Search terms...
search_terms = [ "COVID|Corona" ]

# Subreddits to look in.... (default=ALL)
subreddits = []

# Creating a RedScrap Object
scrapper = RedScrap(start_date=start_date, 
                    end_date=end_date, 
                    search_terms=search_terms,
                    subreddits=subreddit)

# Retrieve submissions...
scrapper.retrieve_submissions(retrieve_comments=False)
```


#### Run main.py

Alter main.py. (Can use command line arguments)

```bash
python main.py
```


## To Do

* Add Support to gather comments only
* Improve code documentation
* Add pip install RedScrap