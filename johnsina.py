from bs4 import BeautifulSoup
import urllib.request
import re

x = str(input("Enter a number, x being the value in http://blog.sina.com.cn/s/article_sort_x_10001_1.html: "))
howmanypages = int(input("How many pages? "))+1

for page in range(1, howmanypages):
    url = 'http://blog.sina.com.cn/s/article_sort_' + x + '_' \
            + '10001_' + str(page) + '.html'
    webpage = urllib.request.urlopen(url)
    soup = BeautifulSoup(webpage, 'html.parser')

    link = soup.find('div', attrs={'class': 'tag SG_txtc'})
    links = soup.find_all('div', {'class': 'tag SG_txtc'})

    print('Page {}: '.format(str(page)) + url + '\n')

    for link in list(links):
        print("Post: "+link.a['href'])
    print()

    myfile = open('posts.txt', 'a')
    for link in links:
        myfile.write("%s\n" % link.a['href'])
    myfile.close()

    file2 = open('pages.txt', 'a')
    file2.write("%s\n" % url)
    file2.close()
