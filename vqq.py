import sys
import os
import re
import json
import wget
import urllib.request
from bs4 import BeautifulSoup

vidid = input("Enter a QQ identifier: ")
url = 'https://v.qq.com/x/page/' + vidid + '.html'
fnameappend = '.info.json'
jsonenc = json.JSONEncoder()
page = urllib.request.urlopen(url)
soup = BeautifulSoup(page, 'html.parser')
title = soup.title.text.strip().replace('_腾讯视频','')

def QQ(url):
    dict = {'vidid': vidid, \
            'origurl': url, \
            'title': title, \
            'description': None, \
            'uploader': None, \
            'channel':None, \
            'uploaded': None}

    dict['description'] = soup.find('meta', attrs={'name': 'description'})['content']
    dict['uploaded'] = soup.find('span', attrs={'class': 'date _date'}).text.strip()
    dict['uploader'] = soup.find('span', attrs={'class': 'user_name'}).text.strip()
    dict['channel'] = soup.find('div', attrs={'class': 'video_user _video_user'}).a['href']

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

QQ(url)


print('\n' + 'Downloading video...')
os.system('you-get ' + url + ' -O "' + title + '"-' + vidid)
print('Done!')
