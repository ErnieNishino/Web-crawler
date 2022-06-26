import requests
import re
import pandas as pd
import datetime

HEADERS = {"User-Agent":" "} #fill the blank with your browser User-Agent
url = "http://renshi.people.com.cn/"
con = requests.get(url, headers=HEADERS).content.decode("GB2312")

p = "<li><a href='(.*)' target=_blank>(.*)</a>  <i>(.*)</i></li>"
l = re.findall(p,con)
#print(l)
news = {}
title = []
href = []
Time = []
for i in l:
    title.append(i[1])
    href.append(i[0])
    Time.append((i[2]))
news["title"] = title
news["href"] = href
news["time"] = Time
#print(news)
df = pd.DataFrame(news)
#print(df)
d= datetime.datetime.now()
y = str(d.year)
m = str(d.month)
da = str(d.day)
name = "peo"+y+m+da+".xlsx"
df.to_excel(name)
