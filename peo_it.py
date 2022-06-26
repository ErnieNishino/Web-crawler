from bs4 import  BeautifulSoup as bs
import datetime
import requests
import pandas as pd

url = "http://it.people.com.cn/GB/243510/index.html"
HEADERS = {"User-Agent":" "} #fill the blank with your browser User-Agent
con = requests.get(url,headers=HEADERS).content.decode("GB2312")
bh = bs(con,"html5lib")
l = bh.find_all("li")
#<li><a href="(.*)" target="_blank">(.*)</a> (.*)</li>
new = {}
title = []
time = []
href = []
for i in l:
    count = 0
    title.append(i.find("a").get_text())
    for j in i:
        c=0
        q=""
        cnt=0
        for k in j:
            if k=="[":
                c=1
            elif c and cnt<11:
                q+=str(k)
                cnt+=1
            elif k=="]":
                time.append(q)
                count = 1
                break
    if count==0:
        time.append(":(")
    href.append(i.find("a").get("href"))
new["title"] = title
new["time"] = time
new["href"] = href
da = datetime.datetime.now()
y = str(da.year)
m = str(da.month)
d = str(da.day)
name = "peo_it"+y+m+d+".xlsx"
df = pd.DataFrame(new)
df.to_excel(name)
print("Done")
