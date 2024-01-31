# coding = utf-8

import os
import requests
from lxml import etree
from bs4 import BeautifulSoup
import pandas as pd
import re
import json
import xlwt

proxies = {
    'http': 'http://127.0.0.1:10809',
    'https': 'http://127.0.0.1:10809'
}
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"}

def get_response(url):
    turns = []
    res = requests.get(url=url,proxies=proxies,headers=headers)
    soup = BeautifulSoup(res.text,'html.parser')
    turns_ = soup.find_all('tr', class_="d-block")
    for turn in turns_:
        dialog = turn.text.replace('\xa0'*4, '\n\n').strip()
        if dialog == "The text was updated successfully, but these errors were encountered:":
            continue
        if not dialog:
            continue
        turns.append(dialog)
    return turns

def get_links(url_base, pages, tag="open"):
    if not url_base.endswith("/"):
        url_base = url_base + '/'
    datas = []
    for page in range(pages+1):
        url = url_base + "issues?page={page}&q=is%3Aissue+is%3A{tag}".format(page=page+1, tag=tag)
        print(url)
        res = requests.get(url=url,proxies=proxies,headers=headers)
        soup = BeautifulSoup(res.text,'html.parser')
        issue_groups = soup.find_all('a', id=re.compile(r'issue_\d+_link'))
        response_groups = soup.find_all('a', class_="Link--muted")
        response_dict = dict()
        for g in response_groups:
            try:
                link = "https://github.com" + g.get("href")
                count = int(g.span.string)
                response_dict[link] = count
            except:
                pass
        if not issue_groups:
            break
        for group in issue_groups:
            link = "https://github.com" + group.get("href")
            title = group.string
            if not title:
                continue
            count = response_dict.get(link, 0)
            turns = get_response(link)
            data = {"url_base":url_base, "source_url":url, "link":link, "title":title, "count":count, "turns":turns}
            datas.append(data)
    return datas

def request_issue(project_url):
    pages = 100
    print("started crawling....", project_url)
    print("started crawling open issues...", project_url)
    open_datas = get_links(url_base=project_url, pages=pages, tag="open")
    print("started crawling closed issues...", project_url)
    closed_datas = get_links(url_base=project_url, pages=pages, tag="closed")
    datas = open_datas + closed_datas
    print("saved issues...", project_url)
    out = open('vacanza_python-holidays_issue.json', 'w+',encoding='utf-8')
    out.write(json.dumps(datas, ensure_ascii=False))
    out.close()
    return