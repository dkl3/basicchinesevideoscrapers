import sys
import urllib.request
import re
import string
import requests
from bs4 import BeautifulSoup

type = input("Enter a QQ Video identifier: ")
url = 'https://v.qq.com/x/page/' + type + '.html'
page = urllib.request.urlopen(url)
# page.geturl() # checks for final url after redirect
soup = BeautifulSoup(page, 'html.parser')

get_uploaddate = soup.find('meta', attrs={'itemprop': 'datePublished'})
uploaddate = get_uploaddate.text.strip()

get_userlink = soup.find("a", href=re.compile("^http://v.qq.com/vplus/[a-z0-9]*$")) # gets the channel url link
userlink = get_userlink.text

page2 = urllib.request.urlopen(get_userlink.get('href'))
soup2 = BeautifulSoup(page2, 'html.parser')
soup2_title = soup2.html.head.title.text.strip()
soup2_uni = soup2_title

soup2new = soup2_uni.replace('- 视频列表', '', 1)

get_desc = soup.find("meta", {"name": "description"})
desc = get_desc.text.strip()

get_username = soup.find('span', attrs={'class': 'user_name'})
username = get_username.text.strip()

get_origurl = soup.find('meta', attrs={'itemprop': 'url'})
origurl = get_origurl.text.strip()

get_title = soup.find('meta', attrs={'itemprop': 'name'})
title = get_title.text.strip()

print("Uploader: " + soup2new + "(Channel: " + get_userlink.get('href') + ")")
print("Upload date: " + get_uploaddate["content"])
print("Description: " + str(get_desc["content"])) # checks the value of content, within meta name=description
print("Original url: " + str(get_origurl["content"]))

uploader_output = "Uploader: " + soup2new + "(Channel: " + get_userlink.get('href') + ")"
uploaded_output = "Upload date: " + get_uploaddate["content"]
desc_output = "Description: " + get_desc["content"]
source_output = "Original url: " + get_origurl["content"]

textfile = get_title["content"] + "-" + type + '-metadata.txt'

variableprintstring = (uploader_output + "\n" + uploaded_output + "\n" + desc_output + "\n" + source_output)
f = open( textfile, 'w' )
f.write(variableprintstring + "\n")
f.close()
