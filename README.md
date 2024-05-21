# Web-crawler
**How to get User-Agent**
--> https://www.whatismybrowser.com/detect/what-is-my-user-agent/

# 轻之文库
## 不时轻声地以俄语遮羞的邻座艾莉同学(時々ボソッとロシア語でデレる隣のアーリャさん)
**aarya.py**

如果没有reportlab或selenium

```python
pip install reportlab
pip install selenium
```

这里填写你的chromedriver地址

```python
webdriver_path = 'chromedriver.exe'
```

**如何获得对应版本的chromedriver？**

chrome122/123/124的浏览器驱动：

https://storage.googleapis.com/chrome-for-testing-public/124.0.6367.155/win64/chromedriver-win64.zip

[ChromeDriver Latest Releases Versions Downloads - Chrome for Testing availability](https://getwebdriver.com/chromedriver)

114版本及之前的浏览器驱动chromedriver：

https://registry.npmmirror.com/binary.html?path=chromedriver/

115及之后的新版本的浏览器驱动：

https://chromedriver.com/

根据自己浏览器的版本来选择驱动，status 要选200的。
复制要选的地址，在浏览器打开即可另存为。
