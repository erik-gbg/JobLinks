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

### joblinks.py
Given a search query this module reads all ads (in successive 
batches of 100). A catalogue is created, grouped by sites, containing 
a subset of the data attributes. The catalogue can be saved as a JSON file
or used directly by the joblinks_browswer.

### joblinks_browswer.py
A very simple GUI for browsing a joblinks catalogue. Implemented with PySimpleGUI.

## Installation
First:

    > pip install -r requirements.txt

Then you need to set the URL of the API used for 
extracting the ads. It should end in `/joblinks`.
There are two ways:
* Put the URL in a file called `joblinks.url`, or
* Edit the URL variable in the source code (two files)

## Running

### test_joblinks_example.py
Is stand-alone. Just make sure the API URL is set, and run.

### joblinks.py
Serves as the data handling module for the joblinks_browser.
If run alone (as main) it will write the data in two JSON files. 
The query string is given as a command line argument ("Python" 
is used as default query).
Also here the API URL needs to be set before running.

Example:

    > python joblinks.py Java

Will create two files:
1. `java catalogue.json` with all ads for query "java"
2. `java catalogue multihits.json` only ads with multiple links

The joblinks_browser can use these files, thus we can avoid asking the API every time.
Or you may browse them with a JSON viewer. The reason for the second file is that "multi hits"
are of special interest for this exercise.

### joblinks_browswer.py

Should be self-explanatory.
