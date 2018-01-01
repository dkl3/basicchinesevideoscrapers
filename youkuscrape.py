# Metadata is sourced from 29bc.com/plus/youku since it displays improperly on the desktop version of Youku.

import sys
import os
import re
import json
import wget
import urllib.request
from selenium import webdriver
from bs4 import BeautifulSoup

vidid = input("Enter a Youku identifier: ")
url = 'http://www.29bc.com/plus/youku/index.php?id=' + vidid
source = 'http://v.youku.com/v_show/id_' + vidid + '.html'
fnameappend = '.info.json'
jsonenc = json.JSONEncoder()
page = urllib.request.urlopen(url)
soup = BeautifulSoup(page, 'html.parser')
title = soup.find("strong", {"class": "v-title vtitle", "yk": "video-title"}).text.strip()

def Youku(url):
    dict = {'vidid': vidid, \
            'origurl': source, \
            'title': title, \
            'description': None, \
            'uploader': None, \
            'channel': None, \
            'uploaded': None}

    browser = webdriver.PhantomJS() # be sure to sudo apt install phantomjs first!
    browser.get(source)
    soup2 = BeautifulSoup(browser.page_source, 'html.parser')

    dict['channel'] = 'http:' + soup2.find('dl', attrs={'id': 'subscription_wrap'}).a['href']
    dict['description'] = soup.find('div', attrs={'class': 'panel-body info-content'}).text.strip()
    get_info = soup.find('ul', attrs={'class': 'list-group info-content'})
    info = get_info.text.strip()
    dict['uploaded'] = get_info.find("span", {"class": "v-published", "yk": "video-published"}).text.strip()
    dict['uploader'] = get_info.find("a", {"class": "v-user", "yk": "user-name"}).text.strip()

    print("Title: " + title)
    print("Uploader: " + dict['uploader'])
    print("Channel: " + dict['channel'])
    print("Upload date: " + dict['uploaded']) # In YYYY-MM-DD format.
    print("Description: " + dict['description'])
    print("Original url: " + source)

    filename=title.translate(str.maketrans("*/\\<>:\"|","--------")).strip()+"-" + vidid + fnameappend
    print(filename)
    print(dict)
    f = open(filename, 'w')
    f.write(jsonenc.encode({dict['vidid']: dict}))
    f.close()
Youku(url)

print('\n' + 'Downloading video...')
os.system('you-get ' + source + ' -O "' + title + '"-' + vidid)
print('Done!')
