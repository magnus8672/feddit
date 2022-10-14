#feddit.py Fetch video from reddit
#magnus8672 9/2022
#A simple Tool for scraping video URLS from a given subreddit
#Use the PARAMS section to change variables for locations of input and output to match your file system layout.
#Remember to escape (bouble slash) any slash "\" characters in your file path as python will otherwise interpreate some combos of a "\" 
#and a letter as a control character and freak the heck out" C:\\some\\dir\\ == good. C:\some\dir\ == bad

from logging import exception
import requests
import os
import json
import time
from datetime import datetime
import logging
from src.config import getconfig

runs = 0

config = getconfig()
#set logging params
logging.basicConfig(level=logging.INFO, filename="feddit.log", filemode="a+", format="%(asctime)-15s %(levelname)-8s %(message)s")
#Get the current time in a file name compatible string
date = datetime.now().strftime("%Y_%m_%d_%I_%M")
logging.info("Feddit Reddit Video Fetcher started running at: " + date)
#Send a request with associated user agent (We just copied some apple one from the interbutts) to get the json which contaisn video links
logging.info("Fetching JSON URL: " + config["baseurl"])

#set up an empty list to itterate into
scrapedids = []
#set an empty array to capture index of 99th child in each json request
nchild = []
#instantiate empty param string to pass for the index so we can get the top page, and subsequenty move to additional pages of json
indexParam = ""
#set a counter so each loop through generating the video will get a unique name
vidcounter = 0

def getJson(indexParam):
    #construct a URL from the base URL + needed URI Params
    url = config.baseurl + ".json?" + indexParam + "limit=100"
    #fire request to get the json including a made up user agent string we googled.
    r = requests.get(url,headers={"User-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36"})
    #cast the content of the json we got to a data object to return for the next function
    d = r.json()
    return d


def getChildren(d):
    #This is based on the structure of reddits json output. We want the fallback URLs of any videos nested under data:children:child(This will be an int 0-25):data:secure_media:reddit_video:fallback_url
    #The try is simply to not care if any children don't have videos as we are not interested in those posts, and I don't care to do a nested if to selectively grab children which contain a video link
    global nchild
    logging.info("Grabbing list of Video URLS from JSON")
    for child in d['data']['children']:
        try:
            scrapedids.append(child["data"]['secure_media']['reddit_video']['fallback_url'])
        except:
            print("encountered an exception with child" )
            echild = str(child["data"]['secure_media'])
            logging.error("A child object in json did not contain a video URL. Video Type was: " + echild)

    #get the 100th childs ID (it starts at 0 so 100th is id 99) We need to this access the "next page of JSON data"
    nchild.append(d["data"]['children'][99]['data']['id'])
    print(str(nchild))

    print (scrapedids)
    logging.info("Finished Scraping URLS \n URL list: ")
    # log out a list of the URL's we identified 
    for vurl in scrapedids:
        svurl = str(vurl)
        logging.info("URL: " + svurl)
    #IDK if I even need to return this value. It's a global and I could just do it that way I guess. But it seems to work so not going to mess with it
    return scrapedids

def makeVideos(scrapedids):
    logging.info("Begin Processing Videos from list:")
    #go get all the video/audio links from the URLs we identified and squish them together into a final video
    for video_url in scrapedids:
        global vidcounter
        #some nonesense to infer the AUDIO URL based on the associated Video URL we gathered
        audio_url = "https://v.redd.it/"+video_url.split("/")[3]+"/DASH_audio.mp4"
        svideourl = str(video_url)
        logging.info("Download Video and audio from: " + svideourl)
        #stuff the video and audio files into aa staging area to be processed with ffmpeg
        videoname = config["rootlocation"] + "video" + str(vidcounter) + ".mp4"
        audioname = config["rootlocation"] + "audio" + str(vidcounter) + ".mp3"
        #open and save the content of the video and audio URLS
        with open(videoname,"wb") as f:
            g = requests.get(video_url,stream=True)
            f.write(g.content)
        with open(audioname,"wb") as f:
            g = requests.get(audio_url,stream=True)
            f.write(g.content)
        #Process audio and video URLS and dump combined output in the target location
        cvidname = config["targetlocation"] + "redditvideo" + date + "_" + str(vidcounter) + ".mp4"
        logging.info("Writing Final video: " + cvidname)    
        os.system(config["ffmpeglocation"] + "ffmpeg.exe -i " +  videoname + " -i "  + audioname + " -c copy " + cvidname)
        #be nice to the reddit servers
        time.sleep(2)
        #increment counter so next video name will not collide with previous video
        vidcounter += 1

def cleanUp():
    #cleanup artifacts when we are done
    for file in os.listdir(config.rootlocation):
        # TODO: un metodo para la limpieza individual
        logging.info("cleaning up " + file)
        print("cleaning up " + file)
        dfile = config["rootlocation"] + file
        os.remove(dfile)

#Main program loop. Call each function in order the configured number of times
while runs < config.runcount:
    #gather JSON Data from URL
    data = getJson(indexParam)
    #find all the Video URLS within the json children
    getChildren(data)
    #set an index of the 99th value from the last page of JSON we gathered
    baseIndex = str(nchild)
    #clean the excess brackets and quotes from the string so it can be part of the next JSON URL
    cleanIndex = baseIndex[2:-2]
    print(cleanIndex)
    logging.info("New JSON Index = " + cleanIndex)
    #set a new index value parameter in the URI so we can get the next 100 json objects after the index
    indexParam = "after=t3_" + cleanIndex + "&"
    #be nice to reddits servers
    time.sleep(2)
    #nullify the index value so it can be re-used in the next loop
    nchild = []
    runNum = str(runs)
    logging.info("Finished Pass number: " + runNum)
    runs += 1

#Make all the videos from the URLS we gathered
makeVideos(scrapedids)
#cleanup all the left over original video and audio files
cleanUp()
