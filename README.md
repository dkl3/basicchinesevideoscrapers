Random simple scrapers for Chinese video hosts, mainly used by BeautifulSoup to get the metadata info. They were created to improve the accuracy of scraping Chinese video sites. These scripts are only compatible with Python 3.

Files:

bilibilivideoandmetadata.py is just a wrapper for getting a video, comments, and metadata using you-get for vid/comments and youtube-dl for the metadata.

iqiyiscrape.py is for scraping metadata, the thumbnail, and downloads a video with youtube-dl.

qqvidscraper.py was made by AcolyteGeometry, and is just included here because.

tudouscraper.py has the same function as iqiyiscrape.py except it's Tudou.

youkuscrape.py is for getting Youku metadata and downloading the video.

Folders:

You-Get Scraper (Youku Videos) was made by zms21. Huge thank you to him, since this gets the you-get filenames with timestamps added at the time. This prevents a file from overriding the other. You must list each link, one by line, in url_list.txt; channel links do not work.

You-Get Scraper (Tudou Videos) is the same except I made it. Could not have been done were it not for zms21's Youku wrapper. :) See the Youku variant for instructions on how to add links. The only accepted syntax is http://video.tudou.com/v/VIDID.html.
