import sys
import os
import urllib.request
import wget
from bs4 import BeautifulSoup

vidid = input("Enter an Iqiyi identifier: ")
url = 'http://www.iqiyi.com/w_' + vidid + '.html'
page = urllib.request.urlopen(url)
soup = BeautifulSoup(page, 'html.parser')

title = soup.find('meta', attrs={'itemprop': 'name'})['content']
origurl = soup.find('meta', attrs={'property': 'og:url'})['content']
description = soup.find('meta', attrs={'itemprop': 'description'})['content']
uploaded = soup.find('meta', attrs={'itemprop': 'uploadDate'})['content']

print('Video name: ',title)
print('Description: ', description)
print('Upload date: ',uploaded)
print('Original url: ',origurl)

titleout = 'Video title: ' + title
descout = 'Description: ' + description
uploaddateout = 'Upload date: ' + uploaded
origurlout = 'Original url: ' + origurl

print ('Downloading thumbnail...')
thumbloc = soup.find('meta', attrs={'property': 'og:image'})['content']
thumbdown = wget.download(thumbloc)

textfile = title + "-" + vidid + '-metadata.txt'
textfile = textfile.translate(str.maketrans("*/\\<>:\"|","--------")).strip()
variableprintstring = (titleout + "\n" + descout + "\n" + uploaddateout + "\n" + origurlout + "\n")
f = open( textfile, 'w' )
f.write(variableprintstring + "\n")
f.close()

print('\n' + 'Downloading video...')
os.system('youtube-dl ' + url + ' -q')
print('Done!')
