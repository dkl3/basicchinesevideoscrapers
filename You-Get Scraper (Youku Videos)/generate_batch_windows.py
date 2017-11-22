from youkuscrape import scrape_youku
import sys
if (len(sys.argv)>1):
    listfile = sys.argv[1]
else:
    listfile = "url_list.txt"

f = open(listfile,"r")
urllist=f.readlines()
f.close()

commandfile = "run.cmd"
f = open(commandfile, 'w')
for i in urllist:
    f.write("you-get "+i.strip()+" -O \""+scrape_youku(i)+"\"\n")
f.close()