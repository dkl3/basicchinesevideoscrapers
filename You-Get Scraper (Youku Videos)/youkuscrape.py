# Metadata is sourced from 29bc.com/plus/youku since it displays improperly on the desktop version of Youku.

import sys
import os
import re
import json
import wget
import urllib.request
from bs4 import BeautifulSoup

#vidid = input("Enter a Youku identifier: ")

def Youku(url):
    vidid = re.search(r'(?:id_)(.*)(?:\.html$)', url, re.I).group(1)
    url = 'http://www.29bc.com/plus/youku/index.php?id=' + vidid
    source = 'http://v.youku.com/v_show/id_' + vidid + '.html'
    fnameappend = '.info.json'
    jsonenc = json.JSONEncoder()

    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    title = soup.find("strong", {"class": "v-title vtitle", "yk": "video-title"}).text.strip()

    dict = {'vidid': vidid, \
            'origurl': source, \
            'title': title, \
            'desc': None, \
            'uploader': None, \
            'uploaded': None}

    dict['desc'] = soup.find('div', attrs={'class': 'panel-body info-content'}).text.strip()
    get_info = soup.find('ul', attrs={'class': 'list-group info-content'})
    info = get_info.text.strip()
    dict['uploaded'] = get_info.find("span", {"class": "v-published", "yk": "video-published"}).text.strip()
    dict['uploader'] = get_info.find("a", {"class": "v-user", "yk": "user-name"}).text.strip()

    print("Title: " + title)
    print("Uploader: " + dict['uploader'])
    print("Upload date: " + dict['uploaded']) # In YYYY-MM-DD format.
    print("Description: " + dict['desc'])
    print("Original url: " + source)

    filename=title.translate(str.maketrans("*/\\<>:\"|","--------")).strip()+"-" + vidid + fnameappend
    print(filename)
    print(dict)
    f = open(filename, 'w')
    f.write(jsonenc.encode({dict['vidid']: dict}))
    f.close()

    vidname = title.translate(str.maketrans("*/\\<>:\"|","--------")).strip()+"-" + vidid

    return vidname
