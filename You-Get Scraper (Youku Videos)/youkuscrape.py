# Metadata is sourced from 29bc.com/plus/youku since it displays improperly on the desktop version of Youku.

import sys
import os
import re
import json
import wget
import urllib3
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from requests import Session, exceptions
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

def Youku(url):
    vidid = re.search(r'(?:id_)(.*)(?:\.html$)', url, re.I).group(1)
    url = 'http://www.29bc.com/plus/youku/index.php?id=' + vidid
    source = 'http://v.youku.com/v_show/id_' + vidid + '.html'
    fnameappend = '.info.json'
    jsonenc = json.JSONEncoder()

    browser = webdriver.PhantomJS() # be sure to sudo apt install phantomjs first!
    browser.set_page_load_timeout(10)
    while True:
        try:
            browser.get(url)
        except TimeoutException:
            print("Timeout, retrying...")
            continue
        else:
            break

    soup = BeautifulSoup(browser.page_source, 'html.parser')
    title = soup.find("strong", {"class": "v-title vtitle", "yk": "video-title"}).text.strip()

    dict = {'vidid': vidid, \
            'origurl': source, \
            'title': title, \
            'description': None, \
            'uploader': None, \
            'channel': None, \
            'uploaded': None}

    browser2 = webdriver.PhantomJS() # be sure to sudo apt install phantomjs first!
    browser2.set_page_load_timeout(10)
    while True:
        try:
            browser2.get(source)
        except TimeoutException:
            print("Timeout, retrying...")
            continue
        else:
            break
    soup2 = BeautifulSoup(browser2.page_source, 'html.parser')

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

    vidname = title.translate(str.maketrans("*/\\<>:\"|","--------")).strip()+"-" + vidid

    return vidname
