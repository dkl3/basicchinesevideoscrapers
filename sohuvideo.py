import sys
import os
import re
import json
import wget
import urllib.request
from selenium import webdriver
from bs4 import BeautifulSoup

url = input("Enter a Sohu URL: ")
vidid = input("Enter video ID, precedes .shtml: ")
fnameappend = '.info.json'
#page = urllib.request.urlopen(url)
#soup = BeautifulSoup(page, 'html.parser')

def Sohu(url):
    
    jsonenc = json.JSONEncoder()
    browser = webdriver.PhantomJS() # be sure to sudo apt install phantomjs first!
    browser.get(url)
    soup = BeautifulSoup(browser.page_source, 'html.parser')

    dict = {'vidid': vidid, \
            'origurl': url, \
            'title': None, \
            'description': None, \
            'uploader': None, \
            'channel':None,\
            'uploaded': None}

    dict['title'] = soup.find('meta', attrs={'property': 'og:title'})['content']
    dict['description'] = soup.find('span', attrs={'class': 'sr h18'}).text.strip()
    dict['uploaded'] = soup.find('span', attrs={'class': 'vbtn vbtn-date'}).text.strip()

    retrieve_uploader = soup.find('p', attrs={'class': 'l'})
    dict['uploader'] = retrieve_uploader.text.strip()
    dict['channel'] = 'http:' + retrieve_uploader.a['href']

    print("Uploader: " + dict['uploader'])
    print("Channel link: " + dict['channel'])
    print("Upload date: " + dict['uploaded'])
    print("Description: " + dict['description'])
    print("Original url: " + url)

    filename=dict['title'].translate(str.maketrans("*/\\<>:\"|","--------")).strip()+"-" + vidid + fnameappend
    print(filename)
    print(dict)
    f = open(filename, 'w')
    f.write(jsonenc.encode({dict['vidid']: dict}))
    f.close()

    print ('Downloading thumbnail...')
    thumbloc = soup.find('meta', attrs={'property': 'og:image'})['content']
    thumbdown = wget.download(thumbloc)
    os.rename(thumbdown,dict['title']+'-'+vidid+'.jpg')

    print('\n' + 'Downloading video...')
    os.system('you-get ' + url + ' -O "' + dict['title'] + '"-' + vidid)
    print('Done!')

Sohu(url)
