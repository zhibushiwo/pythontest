import requests
import os
import time
import threading
import json
import re
from bs4 import BeautifulSoup

def download_page(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0"}
    r=requests.get(url,headers=headers)
    r.encoding='utf-8'
    return r.text


def download(url,tit):
    html=download_page(url)
    with open('layuiadmin/{}'.format(tit+'.html'),'wb') as f:
        f.write(html)
        time.sleep(1)

def get_menu():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0"}
    r=requests.get('http://www.layui.com/admin/pro/json/menu.js?v=1.0.0%20pro&access_token=',headers=headers)
    data=json.loads(r.text,encoding='utf-8')
    for m in data['data']:
        if m.get('list')!=None:
            get_me(m.get('list'),m.get('name'))

def create_dir(name):
    name=name.replace(':','')
    if not os.path.exists(name):
        os.makedirs(name)

def get_me(list,name):
    for l in list:
        if l.get('list')!=None:
            get_me(l.get('list'),name+'/'+l.get('name'))
        else:
            if name!=None:  
                url=name+'/'+ l.get('name')         
                reg=re.compile("(?=/)")
                if len(reg.findall(url))>1:
                    test(url,l.get('title'))
                    continue
                else :
                    test(url+'/'+'index',l.get('title'))

def test(menu,title):
    url='http://www.layui.com/admin/pro/dist/views/'+ menu+'.html?v=1.0.0'
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0"}
    r=requests.get(url,headers=headers)
    r.encoding = 'utf-8'
    soup2 = BeautifulSoup(r.text, 'html.parser')
    t = soup2.title.text
    if t =='好干净的404 - layui':
        print(title)
        return
    create_dir('layuiadmin')
    with open('layuiadmin/{}'.format(title+'.html'),'wb') as f:
        f.write(r.content)
        time.sleep(1)

get_menu()
