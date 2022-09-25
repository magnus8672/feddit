# feddit
feddit.py: A Simple Python tool to Fetch videos from Reddit.

requires os, datetime, logging, requests, json, time, configparser and ffmpeg.exe which you can download here: https://ffmpeg.org/download.html 

Edit feddit.ini to specify file system locations where you have saved ffmpeg.exe, and where to process and store media. Choose a subreddit to pull videos from, and specify how many pages to browse through.

Default Limits to public reddit API force a maximum value of 100 results per page. So if you specify 5 runs in feddit.ini, it will parse through 500 Post results, 100 at a time, and grab all available VIDEO URLS. If you want to go for 1000 results, change runcount to 10. You get the idea. 

It will then take the compiled list of VIDEO Urls and download them each. Then it will call ffmpeg to convert the separate audio and video files into final completed videos. 

By default it will search r/aww. If you want to be gross, put a different subreddit URL in feddit.ini but thats on you. 

The project is based on codenzyme's excellent example: https://github.com/rk26072003/Reddit-Video-downloader-in-13-lines-of-python/blob/main/main.py 
I have used this tool along with another (now deprecated) project for grabbing instagram videos, in order the generate the videos seen here: 
https://youtu.be/agOJJgPTVqc by passing them through my OTHER project Python video compiler: https://github.com/magnus8672/pythonvideocompiler 

If you get error: 
    nchild.append(d["data"]['children'][99]['data']['id'])
IndexError: list index out of range

You might have just run out of posts. Try reducing the size of runcount in feddit.ini
