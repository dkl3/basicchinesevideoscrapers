from bs4 import BeautifulSoup
import sys
import wget
import os
import urllib.request
import re
import json
import subprocess

x = str(input("Enter the url: "))
howmanypages = int(input("How many pages? "))+1

def GetPages():
    for page in range(1, howmanypages):
        webpage = urllib.request.urlopen(x)
        soup = BeautifulSoup(webpage, 'html.parser')
        pagetitle = soup.find('meta', attrs={'property': 'og:title'})['content']
    
        imglink3 = soup.find('meta', attrs={'property': 'og:image'})['content']
        imglink2 = imglink3.replace('1.jpg','')
        imglink = imglink2 + str(page) + ".jpg"
        getimg = wget.download(imglink)
        print('Page {}: '.format(str(page)) + imglink + '\n')

        myfile = open('urls.txt', 'a')
        myfile.write("%s\n" % imglink)
        myfile.close()

        params = ['convert', 'page_*', pagetitle.replace("/",".") + '.pdf']
        subprocess.check_call(params)
    os.system('rm page_*')

def Dict():
    webpage = urllib.request.urlopen(x)
    soup = BeautifulSoup(webpage, 'html.parser')
    fnameappend = '.info.json'
    jsonenc = json.JSONEncoder()
    pagetitle = soup.find('meta', attrs={'property': 'og:title'})['content']
    dict = {'origurl': x, \
            'title': pagetitle, \
            'description': None, \
            'uploader': None, \
            'uploaderlink':None,\
            'uploaded': None}
    dict['description'] = soup.find('meta', attrs={'property': 'og:description'})['content']
    dict['uploaded'] = soup.find('div', attrs={'class': 'DocumentInfo__date--2llaY'})['datetime']
    uploader = soup.find('div', attrs={'class': 'PublisherInfo__name--3j27Y'})
    dict['uploader'] = uploader.text.strip()
    dict['uploaderlink'] = "https://issuu.com/" + dict['uploader']

    webpage2 = urllib.request.urlopen(dict['uploaderlink'])
    soup2 = BeautifulSoup(webpage2, 'html.parser')
    dict['uploadername'] = soup2.find('meta', attrs={'property': 'og:title'})['content']

    filename=pagetitle.translate(str.maketrans("*/\\<>:\"|","--------")).strip()+ fnameappend
    print(dict)
    myfile2 = open(filename, 'w')
    myfile2.write(jsonenc.encode({dict['title']: dict}))
    myfile2.close()

GetPages()
Dict()
