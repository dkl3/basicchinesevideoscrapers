import sys
import os
import re
import json
import wget
import urllib.request
from bs4 import BeautifulSoup

vidid = input("Enter a Tudou identifier: ")
url = 'http://video.tudou.com/v/' + vidid + '.html'
fnameappend = '.info.json'
jsonenc = json.JSONEncoder()
page = urllib.request.urlopen(url)
soup = BeautifulSoup(page, 'html.parser')
title = soup.find('span', attrs={'id': 'subtitle'})['title']

def Tudou():
    dict = {'vidid': vidid, \
            'origurl': url, \
            'title': title, \
            'description': None, \
            'uploader': None, \
            'channel': None, \
            'uploaded': None}

    dict['description'] = soup.find('div', attrs={'class': 'td-play__videoinfo__details-box__desc'}).text.strip()
    uploader = soup.find('a', attrs={'class': 'td-play__userinfo__name'})
    dict['uploader'] = uploader.text.strip()
    dict['channel'] = 'http:' + uploader['href']
    dict['uploaded'] = soup.find('meta', attrs={'name': 'publishedtime'})['content']

    print('Title: ' + dict['title'])
    print('Uploader: ' + dict['uploader'])
    print('Channel link: ' + dict['channel'])
    print('Upload date: ' + dict['uploaded'])
    print('Description: ' + dict['description'])
    print('Original url: ' + dict['origurl'])

    print ('Downloading thumbnail...')
    thumbloc = soup.find('meta', attrs={'name': 'thumb'})['content']
    thumbdown = wget.download(thumbloc)
    os.rename(thumbdown,title+'.jpg')

    filename=title.translate(str.maketrans("*/\\<>:\"|","--------")).strip()+"-" + vidid + fnameappend
    print(filename)
    print(dict)
    f = open(filename, 'w')
    f.write(jsonenc.encode({dict['vidid']: dict}))
    f.close()
Tudou()

print('\n' + 'Downloading video...')
os.system('you-get ' + url + ' -O "' + title + '"-' + vidid)
print('Done!')
