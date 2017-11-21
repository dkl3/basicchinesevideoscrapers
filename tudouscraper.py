import sys
import os
import re
import urllib.request
import wget
from bs4 import BeautifulSoup

vidid = input("Enter a Tudou identifier: ")
url = 'http://video.tudou.com/v/' + vidid + '.html'
page = urllib.request.urlopen(url)
soup = BeautifulSoup(page, 'html.parser')

title = soup.find('span', attrs={'id': 'subtitle'})['title']

uploader = soup.find('a', attrs={'class': 'td-play__userinfo__name'})
uploadername = uploader.text.strip()
channellink = 'http:' + uploader['href']
description = soup.find('div', attrs={'class': 'td-play__videoinfo__details-box__desc'}).text.strip()
uploaddate = soup.find('meta', attrs={'name': 'publishedtime'})['content']

print('Title: ' + title)
print('Uploader: ' + uploadername)
print('Channel link: ' + channellink)
print('Description: ' + description)
print('Upload date: ' + uploaddate)
print('Original url: ' + url)

titleout = 'Title: ' + title
uploaderout = 'Uploader: ' + uploadername
channelout = 'Channel: ' + channellink
descout = 'Description: ' + description
uploadout = 'Upload date: ' + uploaddate
urlout = 'Original url: ' + url

print ('Downloading thumbnail...')
thumbloc = soup.find('meta', attrs={'name': 'thumb'})['content']
thumbdown = wget.download(thumbloc)
os.rename(thumbdown,title+'.jpg')

textfile = title + "-" + vidid + '-metadata.txt'
textfile = textfile.translate(str.maketrans("*/\\<>:\"|","--------")).strip()
variableprintstring = (titleout + "\n" + uploaderout + "\n" + channelout + "\n" + descout + "\n" + uploadout + "\n" + urlout)
f = open( textfile, 'w' )
f.write(variableprintstring + "\n")
f.close()

print('\n' + 'Downloading video...')
os.system('you-get ' + url)
print('Done!')
