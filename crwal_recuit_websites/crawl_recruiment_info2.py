#-*- coding:utf-8 -*-
import requests
import re
from bs4 import BeautifulSoup
import threading
import time
import chardet
import sys
import json

def zhilian_page_link():
    ''''''

    url = 'http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E4%B8%8A%E6%B5%B7&kw=Python&sm=0&p=1'
    req = requests.get(url)
    # print(req)
    page = req.text
    soup = BeautifulSoup(page,'lxml')
    soup_table = soup.find_all('table',attrs={'cellpadding':'0','width':'853','class':'newlist'})
    job_links = []
    for table in soup_table[1:]:
        link_a = table.find_all('a',par=True)
        if len(link_a) > 0:
            job_link = link_a[0]['href']
            job_links.append(job_link)

    return job_links



def zhilian_job_info(job_link):
    '''

    '''
    req = requests.get(job_link)
    page = req.text
    soup = BeautifulSoup(page,'lxml')
    job_dict = {}

    # 基本的信息
    JobName = soup.h1.string
    CompanyName = soup.h2.get_text()
    FirmWebsite = soup.h2.a['href']
    Tags = []

    soup_tags = soup.find('div',attrs={'class':"welfare-tab-box"})
    soup_spans = soup_tags.find_all('span')
    for span in soup_spans:
        span_text = span.string
        Tags.append(span_text)

    job_dict['JobName'] = JobName
    job_dict['CompanyName'] = CompanyName
    job_dict['FirmWebsite'] = FirmWebsite
    job_dict['Tags'] = Tags


    # 职位细节
    soup_ul = soup.find('ul',class_ = 'terminal-ul clearfix')
    for li in soup_ul.find_all('li'):
        key = li.span.string
        value = li.strong.get_text()
        job_dict[key] = value
    # 去除月薪后的符号
    salary = job_dict['职位月薪：']
    y_index = salary.index('月')
    salary = salary[:y_index+1]
    job_dict['职位月薪：'] = salary

    # 岗位职责以及岗位要求
    soup_job_qua = soup.find('div',class_='tab-inner-cont',style=False)
    p_list = []
    for p in soup_job_qua.find_all('p'):
        try:
            element = p.string
            print(element)
        except:
            continue
        else:
            if element:
                p_list.append(element)

    des_index = 0
    qua_index = 0
    for i in p_list:
        if '岗位职责' in i:
            des_index = p_list.index(i)
            print(des_index)
        if '岗位要求' in i:
            qua_index = p_list.index(i)
            print(qua_index)
    # des_index = p_list.index('岗位职责')
    # qua_index = p_list.index('岗位要求')

    job_description = p_list[des_index+1:qua_index]
    job_qualification = p_list[qua_index:]
    job_dict['Description'] = job_description
    job_dict['Qualification'] = job_qualification

    # 工作地点
    key = soup_job_qua.b.string
    value = soup.h2.string.strip()
    job_dict[key] = value


    # 公司简介
    soup_div = soup.find('div',class_="tab-inner-cont",attrs={'style':'display:none;word-wrap:break-word;'})
    firminfo = soup_div.get_text().strip()
    job_dict['FirmInfo'] = firminfo

    # 公司信息
    # <ul class="terminal-ul clearfix terminal-company mt20">
    soup_ul_2 = soup.find('ul',class_="terminal-ul clearfix terminal-company mt20")
    for li in soup_ul_2.find_all('li'):
        key = li.span.string
        value = li.strong.get_text().strip()
        job_dict[key] = value

    print(job_dict)

url = 'http://jobs.zhaopin.com/554362729250983.htm?ssidkey=y&ss=201&ff=03'
zhilian_job_info(url)
