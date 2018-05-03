import sys
import os
import re
import json
import wget
import urllib.request
from selenium import webdriver
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from requests import Session, exceptions
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

vidid = input("Enter a Youku identifier: ")
url = 'http://v.youku.com/v_show/id_' + vidid + '.html'
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
title = soup.find("meta", {"name": "irTitle"})['content']

def Youku(url):
    dict = {'vidid': vidid, \
            'origurl': url, \
            'title': title, \
            'uploader': None, \
            'channel': None, \
            'uploaded': None}

    dict['channel'] = 'http:' + soup.find('span', attrs={'id': 'module_basic_sub'}).a['href']
    dict['uploaded'] = soup.find("span", {"class": "bold mr3"}).text.strip().replace('上传于 ','')
    dict['uploader'] = soup.find("dd", {"class": "dayu-title"}).text.strip()

    print("Title: " + title)
    print("Uploader: " + dict['uploader'])
    print("Channel: " + dict['channel'])
    print("Upload date: " + dict['uploaded']) # In YYYY-MM-DD format.
    print("Original url: " + url)

    filename=title.translate(str.maketrans("*/\\<>:\"|","--------")).strip()+"-" + vidid + fnameappend
    print(filename)
    print(dict)
    f = open(filename, 'w')
    f.write(jsonenc.encode({dict['vidid']: dict}))
    f.close()
Youku(url)

print('\n' + 'Downloading video...')
os.system('you-get ' + url + ' -O "' + title + '"-' + vidid)
print('Done!')
