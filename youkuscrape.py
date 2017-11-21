# Metadata is sourced from 29bc.com/plus/youku since it displays improperly on the desktop version of Youku.

import sys
import os
import wget
import urllib.request
from bs4 import BeautifulSoup

vidid = input("Enter a Youku identifier: ")
url = 'http://www.29bc.com/plus/youku/index.php?id=' + vidid
page = urllib.request.urlopen(url)
soup = BeautifulSoup(page, 'html.parser')

desc = soup.find('div', attrs={'class': 'panel-body info-content'}).text.strip()

get_info = soup.find('ul', attrs={'class': 'list-group info-content'})

info = get_info.text.strip()

uploaded = get_info.find("span", {"class": "v-published", "yk": "video-published"}).text.strip()

uploader = get_info.find("a", {"class": "v-user", "yk": "user-name"}).text.strip()

title = soup.find("strong", {"class": "v-title vtitle", "yk": "video-title"}).text.strip()

source = 'http://v.youku.com/v_show/id_' + vidid + '.html'

print("Title: " + title)
print("Uploader: " + uploader)
print("Upload date: " + uploaded) # In YYYY-MM-DD format.
print("Description: " + desc)
print("Original url: " + source)

title_output = "Title: " + title
uploader_output = "Uploader: " + uploader
uploaded_output = "Upload date: " + uploaded
desc_output = "Description: " + desc
source_output = "Original url: " + source

textfile = title + "-" + vidid + '-metadata.txt'

variableprintstring = (title_output + "\n" + uploader_output + "\n" + uploaded_output + "\n" + desc_output + "\n" + source_output )
f = open( textfile, 'w' )
f.write(variableprintstring + "\n")
f.close()

print('Downloading video...')
os.system('you-get ' + source)
print('Done!')
