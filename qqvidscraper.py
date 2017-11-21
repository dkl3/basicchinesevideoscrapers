#Forked back from AcolyteGeometry.

from MenuT import MenuT
import json
import string
import sys
import requests
import re
from bs4 import BeautifulSoup

class qqVidScraper():

    baseurl = 'https://v.qq.com/x/page/'
    fnameappend = '-metadata.json'
    jsonenc = json.JSONEncoder()
    menut = MenuT()
    menu = [["QQ Video Scraper","Select an option:"],["Scrape Video", 1], ["Exit", 2]]
    menuid = [["QQ Video Scraper", "Input video ID:"]]

    def showMenu(self):
        mopt = self.menut.stoi(self.menut.showMenu(self.menu))
        if(mopt == 1):
            self.vididMenu()
        elif(mopt == 2):
            exit(0)

    def vididMenu(self):
        mopt = self.menut.showMenu(self.menuid)
        self.writeFile(self.scrapeVideo(mopt))
        self.showMenu()

    def scrapeVideo(self, vidid, stdout = True):
        dict = {'vidid': vidid, \
                'title': None, \
                'desc': None, \
                'userlink':None,\
                'username':None, \
                'origurl':None,\
                'date':None}
        url = self.baseurl + vidid + '.html'
        page = requests.get(url, timeout=60).content
        data = json.loads(r.content[len('var videoInfo='):-1])
        # page.geturl() # checks for final url after redirect
        soup = BeautifulSoup(page, 'html.parser')

        dict['username'] = soup.find('span', attrs={'class': 'user_name'}).text.strip()

        dict['userlink'] = soup.find("a", href=re.compile("^http://v.qq.com/vplus/[a-z0-9]*$"))['href']

        get_uploaddate = soup.find('span', attrs={'class': 'date _date'})
        uploaddate = get_uploaddate.text.strip()
        dict['origurl'] = soup.find('meta', attrs={'itemprop': 'url'})['content']
        dict['title'] = soup.find('meta', attrs={'itemprop': 'name'})['content']
        dict['desc'] = soup.find("meta", {"name": "description"})['content']

        page = requests.get(dict['userlink'], timeout=60).content
        if(stdout):
            print("Uploader: " + dict['username'])
            print("Channel: " + dict['userlink'])
            print("Upload Date: " + str(uploaddate))
            print("Description: " + str(dict['desc'])) # checks the value of content, within meta name=description
            print("Original URL: " + str(dict['origurl']))

        return dict

    def writeFile(self, data):
        filename = data['title'] + "-" + data['vidid'] + self.fnameappend
        print(filename)
        print(data)
        f = open(filename, 'w')
        f.write(self.getJSON(data))
        f.close()

    def getJSON(self, data):
        return self.jsonenc.encode({data['vidid']: data})

qqVidScraper().showMenu()
