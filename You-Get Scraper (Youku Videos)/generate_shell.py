from youkuscrape import scrape_youku
import sys
import os

if (len(sys.argv)>1):
    listfile = sys.argv[1]
else:
    listfile = "url_list.txt"

f = open(listfile,"r")
urllist=f.readlines()
f.close()

commandfile = "run.sh"
f = open(commandfile, 'w')
for i in urllist:
    f.write("you-get "+i.strip()+" -O \""+scrape_youku(i).replace(":","-")+"\"\n")
f.close()

os.system('chmod +x run.sh')
os.system('./run.sh')
