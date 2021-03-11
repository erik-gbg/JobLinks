# Joblinks Browser

For browsing Swedish job ads from external sites, 
i.e. not from arbetsformedlingen.se. 
The browser groups the ads by the name of the 
external site. This is just a toy version.

## Requirements
* Python 3.7+

## Source files
### test_joblinks_example.py
This is just a small change to the original file,
according to the given assignment. Now it shows the
links to the ads.

###joblinks.py
Given a search query this module reads all ads (in successive 
batches of 100). A catalogue is created, grouped by sites, containing 
a selection of the data attributes. The catalogue and be saved as a JSON file
or used directly by the joblinks_browswer.

###joblinks_browswer.py
A very simple GUI for browsing a joblinks catalogue.

## Installation
First:

    > pip install -r requirements.txt

Then you need to set the URL of the API used for 
extracting the ads. It should end in /joblinks.
There are two ways:
* Put the URL in a file called joblinks.url, or
* Edit the URL variable in the source code (two files)

## Running






