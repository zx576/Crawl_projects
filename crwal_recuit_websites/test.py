#-*- coding:utf-8 -*-
import requests
import re
from bs4 import BeautifulSoup
import threading
import time
import chardet
import sys
import json

def zhilian_info():
    '''

    '''

    url = 'http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E4%B8%8A%E6%B5%B7&kw=Python&sm=0&p=1'
    req = requests.get(url)
    print(req)
    page = req.text.encode('utf-8')
    # print(chardet.detect(page))
    # print(page)
    # page = json.dumps(page)
    soup = BeautifulSoup(page,'lxml')
    # print(soup.prettify)
    # return soup.prettify
    #<table cellpadding="0" cellspacing="0" width="853" class="newlist">
    soup_table = soup.find_all('table',attrs={'cellpadding':'0','width':'853','class':'newlist'})
    dict_zhilian = {}
    count = 1
    for table in soup_table[1:]:
        dict = {}

        job_title = table.find_all('a',par=True)[0].get_text()
        dict['job_title'] = job_title

        company = table.find_all('td',attrs={'class':'gsmc'})[0]
        if company:
            company_name = company.get_text()
            dict['company_name'] = company_name

            company_url = company.a.href
            dict['company_url'] = company_url

        salary = table.find_all('td',attrs={'class':'zwyx'})[0]
        if salary:
            dict['salary'] = salary.get_text()

        release_date = table.find_all('td',attrs={'class':'gxsj'})[0]
        if release_date:
            dict['release_date'] = release_date.get_text()

        firm_info = table.find_all('li',attrs={'class':"newlist_deatil_two"})[0]
        if firm_info:
            firm_info_span = firm_info.find_all('span')
            for span in firm_info:
                content = span.get_text().split('：')
                dict[content[0]] = content[1]

            job_info = table.find_all('li',attrs={'class':"newlist_deatil_last"})[0]
            if job_info:
                dict['job_info'] = job_info.get_text()
        # print(dict)

        key = 'zhilian'+str(count)
        print(key)
        dict_zhilian[key] = dict
        count += 1

    zhilian_info_str = json.dumps(dict_zhilian)
    with open('zhilian_test.txt','w',encoding='utf-8')as f:
        f.write(zhilian_info_str)
    print('ok')

zhilian_info()


def job51_info():
    '''

    '''
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
    url = 'http://search.51job.com/list/000000%252C00,000000,0000,00,9,99,PYTHON,2,1.html?lang=c&degreefrom=99&stype=1&workyear=99&cotype=99&jobterm=99&companysize=99&radius=-1&address=&lonlat=&postchannel=&list_type=&ord_field=&curr_page=&dibiaoid=0&landmark=&welfare='
    req = requests.get(url)
    page = req.text
    print(page)

# job51_info()
