from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import time
from sys import exit

# 初始化Selenium WebDriver
webdriver_path = 'chromedriver.exe'
service = ChromeService(executable_path=webdriver_path)
driver = webdriver.Chrome(service=service)

# 目标网站的基地址
base_url = 'https://www.wenkuchina.com/lightnovel/4/'

# 设置ReportLab PDF
pdfmetrics.registerFont(TTFont('STSONG', 'STSONG.ttf'))
c = canvas.Canvas("crawled_data.pdf", pagesize=A4)


def fetch_page(url):
    driver.get(url)
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.volume, div.mlfy_main")))
        return driver.page_source
    except TimeoutException:
        print("页面加载超时：", url)
        return None


def parse_catalog(html):
    soup = BeautifulSoup(html, 'html.parser')
    # 选择所有章节链接
    chapters = [a['href'] for a in soup.select('li.col-4 > a')]
    return chapters


def is_illustration_page(soup):
    # 检查是否是插图页面
    h1_text = soup.select_one('h1').get_text()
    return "插图" in h1_text


def wrap_text(text, width):
    current_line = ""
    count = 0  # 当前行的字符计数器
    result = []  # 用于存储所有行的列表

    for char in text:
        if char == "\n":
            # 如果遇到原有的换行符，输出当前行并重置计数器
            if current_line:
                result.append(current_line)
            result.append("\n")
            current_line = ""
            count = 0
        else:
            current_line += char
            count += 1
            if count == width:
                # 如果达到40个字符，添加换行符，输出当前行并重置计数器
                result.append(current_line + "\n")
                current_line = ""
                count = 0

    # 输出最后的内容（如果有）
    if current_line:
        result.append(current_line)

    # 将列表中的所有行合并为一个字符串
    return ''.join(result)


def handle_text_wrapping(canvas, text, start_x, start_y, font_name, font_size, line_limit=51):
    canvas.setFont(font_name, font_size)
    text_object = canvas.beginText(start_x, start_y)
    lines = text.split('\n')
    line_count = 0

    for line in lines:
        if line_count >= line_limit:  # 检查是否需要新建一页
            canvas.drawText(text_object)
            canvas.showPage()  # 创建新的一页
            canvas.setFont(font_name, font_size)
            text_object = canvas.beginText(start_x, start_y)  # 重新开始新的文本对象
            line_count = 0

        text_object.textLine(line)  # 添加当前行到文本对象
        line_count += 1

    # 绘制最后一批文本
    if line_count > 0:
        canvas.drawText(text_object)
        canvas.showPage()


def parse_chapter(html, url):
    soup = BeautifulSoup(html, 'html.parser')
    if is_illustration_page(soup):
        next_chapter = soup.select_one('p.mlfy_page a:-soup-contains("下一章")')
        if next_chapter:
            next_url = next_chapter['href']
            next_html = fetch_page(next_url)
            if next_html:
                parse_chapter(next_html, next_url)
        return

    chapter_title = soup.select_one('h1').get_text()
    text_content = soup.select_one('#TextContent').get_text(separator="\n", strip=True)
    # 在插入每40个字符后自动加入换行符
    text_content = wrap_text(text_content, 40)

    # 写入标题和内容
    c.setFont('STSONG', 12)
    c.drawString(100, 800, chapter_title)  # 调整标题位置
    handle_text_wrapping(c, text_content, 40, 780, 'STSONG', 12)

    # 处理下一页或下一章节
    next_page = soup.select_one('p.mlfy_page a:-soup-contains("下一页")')
    next_chapter = soup.select_one('p.mlfy_page a:-soup-contains("下一章")')
    if next_page:
        next_url = next_page['href']
        next_html = fetch_page(next_url)
        if next_html:
            parse_chapter(next_html, next_url)
    elif next_chapter:
        next_url = next_chapter['href']
        if 'lastchapter.php' in next_url:
            c.save()
            driver.quit()
            print("爬取和PDF创建完成。")
            exit(0)
        else:
            next_html = fetch_page(next_url)
            if next_html:
                parse_chapter(next_html, next_url)


def crawl_chapter(url):
    html = fetch_page(url)
    if html:
        parse_chapter(html, url)
    time.sleep(1)


# 从目录页开始爬取
catalog_html = fetch_page(base_url + 'catalog')
if catalog_html:
    chapter_urls = parse_catalog(catalog_html)
    for url in chapter_urls:
        crawl_chapter(url)
