import sys
import os
import re
import json
import wget
import retry
import urllib3
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from requests import Session, exceptions
from bs4 import BeautifulSoup

def Tudou(url):
    vidid = re.search(r'(?:\/v\/)(.*)(\.html)', url, re.I).group(1)
    url = 'http://video.tudou.com/v/' + vidid + '.html'
    fnameappend = '.info.json'
    jsonenc = json.JSONEncoder()
    s = Session()
    s.mount('https://', HTTPAdapter(
    max_retries=Retry(total=5, status_forcelist=[500, 502, 503])
        )
    )

    page = s.get(url).text
    soup = BeautifulSoup(page, 'html.parser')
    title = soup.find('span', attrs={'id': 'subtitle'}).text.strip()

    dict = {'vidid': vidid, \
            'origurl': url, \
            'title': title, \
            'description': None, \
            'uploader': None, \
            'channel': None, \
            'uploaded': None}

    uploader = soup.find('a', attrs={'class': 'td-play__userinfo__name'})
    dict['uploader'] = uploader.text.strip()
    dict['channel'] = uploader['href']
    dict['description'] = soup.find('div', attrs={'class': 'td-play__videoinfo__details-box__desc'}).text.strip()
    dict['uploaded'] = soup.find('div', attrs={'class': 'td-play__videoinfo__details-box__time'}).text.strip()

    print('Title: ' + dict['title'])
    print('Uploader: ' + dict['uploader'])
    print('Channel link: ' + dict['channel'])
    print('Description: ' + dict['description'])
    print('Upload date: ' + dict['uploaded'])
    print('Original url: ' + dict['origurl'])

    filename=title.translate(str.maketrans("*/\\<>:\"|","--------")).strip()+"-" + vidid + fnameappend
    print(filename)
    print(dict)
    f = open(filename, 'w')
    f.write(jsonenc.encode({dict['vidid']: dict}))
    f.close()

    vidname = title.translate(str.maketrans("*/\\<>:\"|","--------")).strip()+"-" + vidid

    return vidname
