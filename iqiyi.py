import sys
import os
import re
import json
import wget
import urllib.request
from bs4 import BeautifulSoup

vidid = input("Enter an Iqiyi identifier: ")
url = 'http://www.iqiyi.com/w_' + vidid + '.html'
fnameappend = '.info.json'
jsonenc = json.JSONEncoder()
page = urllib.request.urlopen(url)
soup = BeautifulSoup(page, 'html.parser')
title = soup.find('meta', attrs={'itemprop': 'name'})['content']

def Iqiyi(url):
    dict = {'vidid': vidid, \
            'origurl': url, \
            'title': title, \
            'description': None, \
            'uploader': None, \
            'channel':None,\
            'uploaded': None}

    dict['description'] = soup.find('p', attrs={'itemprop': 'description'})['daat-init-moredesc']
    dict['uploaded'] = soup.find('meta', attrs={'itemprop': 'uploadDate'})['content']

    retrieve_uploader = soup.find('a', attrs={'class': 'mod-dyDs-name-link'})
    dict['uploader'] = retrieve_uploader['title']
    dict['channel'] = retrieve_uploader['href']

    print("Title: " + title)
    print("Uploader: " + dict['uploader'])
    print("Channel link: " + dict['channel'])
    print("Upload date: " + dict['uploaded'])
    print("Description: " + dict['description'])
    print("Original url: " + url)

    filename=title.translate(str.maketrans("*/\\<>:\"|","--------")).strip()+"-" + vidid + fnameappend
    print(filename)
    print(dict)
    f = open(filename, 'w')
    f.write(jsonenc.encode({dict['vidid']: dict}))
    f.close()

    print ('Downloading thumbnail...')
    thumbloc = soup.find('meta', attrs={'itemprop': 'thumbnailUrl'})['content']
    thumbdown = wget.download(thumbloc)
    os.rename(thumbdown,title+'-'+vidid+'.jpg')

    print('\n' + 'Downloading video...')
    os.system('you-get ' + url + ' -O "' + title + '"-' + vidid)
    print('Done!')

Iqiyi(url)
