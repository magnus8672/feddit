#feddit.py Fetch video from reddit
#magnus8672 9/2022
#A simple Tool for scraping video URLS from a given subreddit
#Use the PARAMS section to change variables for locations of input and output to match your file system layout.
#Remember to escape (bouble slash) any slash "\" characters in your file path as python will otherwise interpreate some combos of a "\" 
#and a letter as a control character and freak the heck out" C:\\some\\dir\\ == good. C:\some\dir\ == bad

import requests
import os
import time
from datetime import datetime
import logging
from config.parser import get_config
from filesystem.directory import clean
from reddit.parser import get_json, get_videos
from reddit.videos import create_all

# TODO: config and scrapedids to main
config = get_config()
# set up an empty list to itterate into
scraped_ids = []


def main():
    runs = 0
    # set logging params
    logging.basicConfig(level=logging.INFO, filename="feddit.log", filemode="a+",
                        format="%(asctime)-15s %(levelname)-8s %(message)s")
    # Get the current time in a file name compatible string
    date = datetime.now().strftime("%Y_%m_%d_%I_%M")
    logging.info("Feddit Reddit Video Fetcher started running at: " + date)
    # Send a request with associated user agent (We just copied some apple one from the interbutts) to get the reddit which contaisn video links
    logging.info("Fetching JSON URL: " + config["baseurl"])

    # set an empty array to capture index of 99th child in each reddit request
    nchild = []
    params = {}
    # set a counter so each loop through generating the video will get a unique name
    vidcounter = 0

    #Main program loop. Call each function in order the configured number of times
    while runs < config.runcount:
        #gather JSON Data from URL
        data = get_json(params)
        #find all the Video URLS within the reddit children
        scrapedids = get_videos(data)
        #set an index of the 99th value from the last page of JSON we gathered
        baseIndex = str(nchild)
        #clean the excess brackets and quotes from the string so it can be part of the next JSON URL
        cleanIndex = baseIndex[2:-2]
        print(cleanIndex)
        logging.info("New JSON Index = " + cleanIndex)
        #set a new index value parameter in the URI so we can get the next 100 reddit objects after the index
        params['after'] = f"t3_{cleanIndex}"
        #be nice to reddits servers
        time.sleep(2)
        #nullify the index value so it can be re-used in the next loop
        nchild = []
        runNum = str(runs)
        logging.info("Finished Pass number: " + runNum)
        runs += 1

    #Make all the videos from the URLS we gathered
    create_all(scrapedids)
    #cleanup all the left over original video and audio files
    clean(config["rootlocation"])


main()
