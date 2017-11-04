#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import sys
import urllib2
from bs4 import BeautifulSoup

type = raw_input("Enter a Youku identifier: ")
url = 'http://www.29bc.com/plus/youku/index.php?id=' + type
page = urllib2.urlopen(url)
soup = BeautifulSoup(page, 'html.parser')

desc_get = soup.find('div', attrs={'class': 'panel-body info-content'})
desc = desc_get.text.strip()

get_info = soup.find('ul', attrs={'class': 'list-group info-content'})
info = get_info.text.strip()

get_uploaded = get_info.find("span", {"class": "v-published", "yk": "video-published"})
uploaded = get_uploaded.text.strip()

get_uploader = get_info.find("a", {"class": "v-user", "yk": "user-name"})
uploader = get_uploader.text.strip()

source = 'http://v.youku.com/v_show/id_' + type + '.html'

print "Uploader: " + uploader
print "Upload date: " + uploaded # In YYYY-MM-DD format.
print "Description: " + desc
print "Original url: " + source

uploader_output = "Uploader: " + uploader.encode('utf8', 'replace')
uploaded_output = "Upload date: " + uploaded.encode('utf8', 'replace')
desc_output = "Description: " + desc.encode('utf8', 'replace')
source_output = "Original url: " + source.encode('utf8', 'replace')

get_title = soup.find("strong", {"class": "v-title vtitle", "yk": "video-title"})
title = get_title.text.strip()

textfile = title + "-" + type + '-metadata.txt'

variableprintstring = (uploader_output + "\n" + uploaded_output + "\n" + desc_output + "\n" + source_output )
f = open( textfile, 'w' )
f.write(variableprintstring + "\n")
f.close()
