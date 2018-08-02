import requests
import os
import time
import threading
from bs4 import BeautifulSoup


def download_page(url):
    '''
    用于下载页面
    '''
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0"}
    r = requests.get(url, headers=headers)
    r.encoding = 'utf-8'
    return r.text


def get_pic_list(html):
    '''
    获取每个页面的套图列表,之后循环调用get_pic函数获取图片
    '''
    soup = BeautifulSoup(html, 'html.parser')
    pic_list = soup.find_all('div',class_='picbox')
    for pic in pic_list:
        link = pic.find('a').get('href')
        text = pic.find('img').get('alt')
        text=text.replace(':','')
        get_url_list(link, text)
        
    # for i in pic_list:
    #     a_tag = i.find('a')
    #     link = a_tag.get('href')
    #     text = a_tag.find('img').get('alt')
    #     text=text.replace(':','')
        # get_pic(link, text)

def get_url_list(link,text):
    get_pic(link, text)
    html = download_page(link)
    soup = BeautifulSoup(html, 'html.parser')
    span =soup.find('span',text='下一页')
    if(span!=None):
        a_tag = span.parent
        get_url_list(a_tag.get('href'), text)


def get_pic(link, text):
    '''
    获取当前页面的图片,并保存
    '''
    html = download_page(link)  # 下载界面
    html=html.replace('<div class="picture_txt"> </p>','<div class="picture_txt">')
    soup2 = BeautifulSoup(html, 'html.parser')
    pic_list2 = soup2.find('div', id="eFramePic").find_all('img')  # 找到界面所有图片
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0"}
    create_dir('pic/{}'.format(text))
    for i in pic_list2:
        pic_link = i.get('src')  # 拿到图片的具体 url
        r = requests.get(pic_link, headers=headers)  # 下载图片，之后保存到文件
        with open('pic/{}/{}'.format(text, pic_link.split('/')[-1]), 'wb') as f:
            f.write(r.content)
            time.sleep(1)   # 休息一下，不要给网站太大压力，避免被封


def create_dir(name):
    name=name.replace(':','')
    if not os.path.exists(name):
        os.makedirs(name)


def execute(url):
    page_html = download_page(url)
    get_pic_list(page_html)


def main():
    create_dir('pic')
    queue = [i for i in range(1088, 1089)]   # 构造 url 链接 页码。
    threads = []
    while len(queue) > 0:
        for thread in threads:
            if not thread.is_alive():
                threads.remove(thread)
        while len(threads) < 1 and len(queue) > 0:   # 最大线程数设置为 5
            cur_page = queue.pop(0)
            url = 'http://www.k00088.com/xinggan/'
            thread = threading.Thread(target=execute, args=(url,))
            thread.setDaemon(True)
            thread.start()
            print('{}正在下载{}页'.format(threading.current_thread().name, cur_page))
            threads.append(thread)


if __name__ == '__main__':
    execute('http://www.k00088.com/qingchun/')