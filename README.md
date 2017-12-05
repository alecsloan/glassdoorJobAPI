glassdoorJobAPI
===============

## About
This is a project I used to help myself learn some python.
    
This script will scrape job listings off of Glassdoor and get you information such as: Title of Job, Company, Location, Description (HTML), etc.

I'm a senior CS student who's fairly new to professional software development and even Github. So if you have any suggestions, advice, or comments feel free to connect via LinkedIn or Email.
I'm also looking for a job, so that's one of the motivations for me developing this script ;). Note: this is an older version of what I use for my website (Soon to be launched), which inserts directly to MySQL. So if you need help converting the script to insert to your DB just let me know and I'll help!
## Install
Clone:

    $ git clone https://github.com/alecsloan/glassdoorJobAPI 
## Usage
Context:
    
    $ python jobs.py job level count
    Examples:
    $ python jobs.py "software engineer new grad" "all" 30
    $ python jobs.py "software engineer" "entry level" 60
    
Notes:

    - Jobs pull in increments of 30 (amount that Glassdoor displays on each page)
    - Json folder is needed by default to hold the json files. You could change this in script if you want
