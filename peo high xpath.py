from lxml import etree #you should pip install lxml frist
import datetime
import pandas as pd
import requests

url = "http://cpc.people.com.cn/GB/64093/64094/index.html"
HEADERS = {"User-Agent":" "} #fill the blank with your browser User-Agent
con = requests.get(url,headers=HEADERS).content.decode("GB2312")
eH = etree.HTML(con)
l = eH.xpath("//div[@class='fl']/ul/li")
new = {}
title = []
time = []
href = []
#<li><a href='(.*)' target=_blank>(.*)</a>  <i>(.*)</i></li>
for li in l:
    title.append(li.xpath("./a")[0].text)
    time.append(li.xpath("./i")[0].text)
    href.append(li.xpath("./a/@href"))
new["title"] = title
new["time"] = time
new["href"] = href
df = pd.DataFrame(new)
da = datetime.datetime.now()
y = str(da.year)
m = str(da.month)
d = str(da.day)
name = "peo high"+y+m+d+".xlsx"
df.to_excel(name)
print("Done")
