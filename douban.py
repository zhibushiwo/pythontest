import requests
import os
import time
import threading
from bs4 import BeautifulSoup

def download_page(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0"}
    headers={"User-Agent":"Mozilla/5.0"}
    r=requests.get(url,headers=headers)
    r.encoding='utf-8'
    return r.text

def get_list(html):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0"}
    soup=BeautifulSoup(html,'html.parser')
    pic_list=soup.find_all('div',class_='pic')
    if not os.path.exists('douban'):
        os.makedirs('douban')
    for pic in pic_list:
        num = pic.find('em').text
        img_tag = pic.find('img')
        img =img_tag.get('src')
        alt =img_tag.get('alt')
        r = requests.get(img,headers=headers)
        with open('douban/{}'.format(num+'_'+alt+'.jpg'),'wb') as f:
            f.write(r.content)
            time.sleep(3)

def execute(url):
    page_html = download_page(url)
    get_list(page_html)

def main():
    pages=[ i for i in range(225,250,25)]
    for i in pages:
        url = 'https://movie.douban.com/top250?start={}'.format(i)
        execute(url)

main()
