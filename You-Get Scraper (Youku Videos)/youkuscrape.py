# Metadata is sourced from 29bc.com/plus/youku since it displays improperly on the desktop version of Youku.

import sys
import urllib.request
from bs4 import BeautifulSoup
import re

def scrape_youku(url):
    #type = input("Enter a Youku identifier: ")
    type = re.search(r'(?:id_)(.*)(?:==.*)', url, re.I).group(1)
    
    url = 'http://www.29bc.com/plus/youku/index.php?id=' + type
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')

    title_get = soup.find("strong", {"class": "v-title vtitle", "yk": "video-title"})
    title = title_get.text.strip()

    title_get = soup.find('div', attrs={'class': 'panel-heading toggleinfo'})
    title = title_get.text.strip()

    desc_get = soup.find('div', attrs={'class': 'panel-body info-content'})
    desc = desc_get.text.strip()

    get_info = soup.find('ul', attrs={'class': 'list-group info-content'})
    info = get_info.text.strip()

    get_uploaded = get_info.find("span", {"class": "v-published", "yk": "video-published"})
    uploaded = get_uploaded.text.strip()

    get_uploader = get_info.find("a", {"class": "v-user", "yk": "user-name"})
    uploader = get_uploader.text.strip()

    source = 'http://v.youku.com/v_show/id_' + type + '.html'
    
    
    filename=title.translate(str.maketrans("*/\\<>:\"|","--------")).strip()+" "+uploaded

    print("Title: " + title)
    print("Uploader: " + uploader)
    print("Upload date: " + uploaded) # In YYYY-MM-DD format.
    print("Description: " + desc)
    print("Original url: " + source)
    print("Filename: " + filename)
    print("\n")

    uploader_output = "Uploader: " + uploader
    uploaded_output = "Upload date: " + uploaded
    desc_output = "Description: " + desc
    source_output = "Original url: " + source

    textfile = title + "-" + type + '-metadata.txt'
    textfile = textfile.translate(str.maketrans("*/\\<>:\"|","--------")).strip()
    variableprintstring = (uploader_output + "\n" + uploaded_output + "\n" + desc_output + "\n" + source_output )
    f = open( textfile, 'w' )
    f.write(variableprintstring + "\n")
    f.close()
    
    return filename

