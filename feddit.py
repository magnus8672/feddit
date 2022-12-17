#feddit.py Fetch video from reddit
#magnus8672 9/2022
#A simple Tool for scraping video URLS from a given subreddit
#Use the PARAMS section to change variables for locations of input and output to match your file system layout.
#Remember to escape (bouble slash) any slash "\" characters in your file path as python will otherwise interpreate some combos of a "\" 
#and a letter as a control character and freak the heck out" C:\\some\\dir\\ == good. C:\some\dir\ == bad

import time
from datetime import datetime
import logging
from pprint import pformat

from config.parser import get_config
from filesystem.directory import clean
from reddit.parser import get_json, extract_next_index, extract_video_url, MissingNextIndexException
from reddit.videos import create_all


def main():
    config = get_config()
    scraped_urls = []
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
    params = {}
    run_count = int(config['run_count'])
    #Main program loop. Call each function in order the configured number of times
    while runs < run_count:
        #gather JSON Data from URL
        logging.info("Grabbing list of Video URLS from JSON")
        response = get_json(params)
        videos = response['data']['children']
        #find all the Video URLS within the reddit children
        logging.info("Grabbing list of Video URLS from JSON")
        scraped_urls += extract_video_url(videos)
        #set a new index value parameter in the URI so we can get the next 100 reddit objects after the index
        next_index = get_next_index(response)
        params['after'] = next_index
        print(next_index)
        logging.info("New JSON Index = " + next_index)
        #be nice to reddits servers
        time.sleep(2)
        #nullify the index value so it can be re-used in the next loop
        nchild = []
        logging.info("Finished Pass number: " + str(runs))
        runs += 1

    logging.info("Finished Scraping URLS \n URL list: %s", pformat(scraped_urls))
    #Make all the videos from the URLS we gathered
    logging.info("Begin Processing Videos from list:")
    create_all(scraped_urls)
    #cleanup all the left over original video and audio files
    clean(config["rootlocation"])


def get_next_index(response):
    try:
        return extract_next_index(response)
    except MissingNextIndexException:
        return ""


main()
