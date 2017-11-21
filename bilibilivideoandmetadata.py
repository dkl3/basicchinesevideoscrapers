import os

id = input("Enter the BiliBili identifier, begins with \'av\': ")

os.system('you-get ' + 'http://www.bilibili.com/video/' + id)
os.system('youtube-dl ' + 'http://www.bilibili.com/video/' + id + ' --write-info-json --write-thumbnail --write-description --write-annotations --skip-download')
