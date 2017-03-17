#-*- coding:utf-8 -*-
import requests
import re
from bs4 import BeautifulSoup
import threading
import time
import chardet
import sys
import json
from recruitment_info_dt import Tackle_dt
# from practice import dict1
from queue import Queue
# import multiprocessing
# import implement_ip_dt
# import fetch_ip
# import pickle

# q_fetch_url = Queue()

'''抓取详细信息的 队列'''
q_fetch_info = Queue()

def req_zhilian(url,status):
    '''请求智联网址

    proxy - 代理，担心免费 ip 的性能，先用 none
    status - 1 标示抓取链接的请求 2 标识抓取信息的请求

    '''
    global q_fetch_info
    req = requests.get(url)
    if req.status_code == 200:
        return req.text
    else:
        if status == 2:
            q_fetch_info.put(url)



def zhilian_page_link(page,end_day):
    '''抓取链接

    page - 请求后返回的文本内容
    end_day - 抓取截止的一天

    '''

    soup = BeautifulSoup(page,'lxml')
    soup_table = soup.find_all('table',attrs={'cellpadding':'0','width':'853','class':'newlist'})
    job_links = []
    for table in soup_table[1:]:
        link_a = table.find_all('a',par=True)
        date = table.find('td',class_='gxsj').get_text()
        if len(link_a) > 0 and not end_day in date:
            job_link = link_a[0]['href']
            job_links.append(job_link)

    return job_links

def judge_req(page,end_day):
    '''判断抓取链接结束的标志

    page - 请求后返回的文本内容
    end_day - 抓取截止的一天

    '''
    soup = BeautifulSoup(page,'lxml')
    date_td = soup.find_all('td',class_="gxsj")
    # date_td = soup_table
    if 'end_day' in date_td:
        return True
    else:
        return False

def clear(info):
    '''清楚一些多余的字符

    info - 待处理的字符串

    '''
    try:
        info1 = info.replace('\\xa0','').replace('\\t', '').replace('\\r', '').replace('\\n', '')
        info2 = info1.replace('\xa0','').replace('\t', '').replace('\r', '').replace('\n', '')
        info3 = info2.replace('\"','').replace('\'','')
    except:
        return info
    return info3




def zhilian_job_info(page):
    '''清洗网页体内容，提取有效信息，返回字典格式的数据

    page - 字符串形式的网页内容

    '''
    soup = BeautifulSoup(page,'lxml')
    job_dict = {}
    job_dict['Resource'] = '智联招聘'
     # 基本的信息
    JobName = clear(soup.h1.string)
    CompanyName = clear(soup.h2.get_text())

    FirmWebsite = soup.h2.a['href']
    Tags = []

    soup_tags = soup.find('div',attrs={'class':"welfare-tab-box"})
    soup_spans = soup_tags.find_all('span')
    for span in soup_spans:
        span_text = clear(span.string)
        Tags.append(span_text)

    job_dict['JobName'] = JobName
    job_dict['CompanyName'] = CompanyName
    job_dict['FirmWebsite'] = FirmWebsite
    job_dict['Tags'] = Tags
    # 职位细节
    soup_ul = soup.find('ul',class_ = 'terminal-ul clearfix')
    # print(soup_ul)
    for li in soup_ul.find_all('li'):
        key = clear(li.span.string)
        value = clear(li.strong.get_text())
        job_dict[key] = value
    # 去除月薪后的符号
    # salary = job_dict['职位月薪：']
    # y_index = 0
    # y_index = salary.index('月')
    #
    # salary = salary[:y_index+1]
    # job_dict['职位月薪：'] = salary

    # 岗位职责以及岗位要求
    soup_job_qua = soup.find('div',class_='tab-inner-cont',style=False)
    p_list = []
    for p in soup_job_qua.find_all('p'):
        try:
            element = clear(p.get_text())
        except:
            continue
        else:
            if element:
                p_list.append(element)
    # print(p_list)
    des_index = 0
    qua_index = None
    for i in p_list:
        if '岗位职责' in i or '工作职责' in i or '职责描述' in i:
            des_index = p_list.index(i)
            # print(des_index)

        if '岗位要求' in i or '任职要求' in i \
            or '职责要求' in i or '岗位基本要求' in i or '任职资格' in i:
            qua_index = p_list.index(i)
            # print(qua_index)
    job_description = None
    job_qualification = None
    if des_index != None:
        job_description = p_list[des_index+1:qua_index]
    if qua_index != None:
        job_qualification = p_list[qua_index+1:]

    job_dict['Description'] = job_description
    job_dict['Qualification'] = job_qualification

    # 工作地点
    key = clear(soup_job_qua.b.string)

    value = clear(soup.h2.string)
    if value:
        value = value.strip()
    job_dict[key] = value
    # 公司简介
    soup_div = soup.find('div',class_="tab-inner-cont",attrs={'style':'display:none;word-wrap:break-word;'})
    firminfo = clear(soup_div.get_text())
    job_dict['FirmInfo'] = firminfo

    # 公司信息
    # <ul class="terminal-ul clearfix terminal-company mt20">
    soup_ul_2 = soup.find('ul',class_="terminal-ul clearfix terminal-company mt20")
    for li in soup_ul_2.find_all('li'):
        key = clear(li.span.string)
        value = clear(li.strong.get_text())
        job_dict[key] = value

    # print(job_dict)
    return job_dict

def insert_info(job_dict):
    '''处理清洗后的内容，返回列表形式有序的数据

    job_dict - 清洗后的数据

    '''
    # pass
    list_d = []
    # job_dict = job_dict
    all_keys = job_dict.keys()

    pri_keys = {'公司主页：', 'Description', 'Resource', '公司行业：', '工作地点：',
    '职位月薪：', '工作经验：', '招聘人数：', 'Qualification', 'Tags', '公司地址：',
     '工作性质：', 'CompanyName', 'JobName', '最低学历：', '公司性质：',
      '公司规模：',  'FirmInfo', '发布日期：'}

    mix_keys = pri_keys - all_keys

    if len(mix_keys) > 0:
        for i in mix_keys:
            job_dict[i] = '缺省'


    for key in all_keys:
        list_d.append(job_dict['Resource'])
        list_d.append(job_dict['JobName'])
        tags = ';'.join(job_dict['Tags'])
        list_d.append(tags)
        list_d.append(job_dict['职位月薪：'])
        list_d.append(job_dict['发布日期：'])
        list_d.append(job_dict['工作经验：'])
        list_d.append(job_dict['招聘人数：'])
        list_d.append(job_dict['工作地点：'])
        list_d.append(job_dict['公司性质：'])
        list_d.append(job_dict['最低学历：'])
        list_d.append(job_dict['Description'])
        list_d.append(job_dict['Qualification'])
        list_d.append(job_dict['CompanyName'])
        list_d.append(job_dict['公司规模：'])
        list_d.append(job_dict['公司行业：'])
        list_d.append(job_dict['公司性质：'])
        list_d.append(job_dict['公司主页：'])
        list_d.append(job_dict['公司地址：'])
        list_d.append(job_dict['FirmInfo'])

    return list_d

def save_info(list_info):
    '''保存信息'''
    tackle_dt = Tackle_dt()
    tackle_dt.insert_info(list_info)


def add_url(url_list):
    '''将抓下来的 url 加入到列表中'''
    global q_fetch_info
    for i in url_list:
        if 'http://' in i:
            # print('ok')
            q_fetch_info.put(i)

def thread_fetch_url(end_day='02-17'):
    '''进程:抓取智联网页，添加链接到队列'''

    base_url = 'http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E4%B8%8A%E6%B5%B7&kw=Python&sm=0&p='
    page_num = 1

    while True:
        url = base_url+str(page_num)
        # print(url)
        req_info = req_zhilian(url,status=1)
        if judge_req(req_info,end_day):
            break
        url_list = zhilian_page_link(req_info,end_day)
        # print(url_list)
        add_url(url_list)
        page_num += 1
        time.sleep(1)
        print('link_on_going')

def thread_fetch_info():
    '''线程：抓取职位信息并保存'''
    global q_fetch_info
    print(q_fetch_info.qsize())
    print('in thread_fetch_info')
    while True:
        # if q_fetch_info.qsize == 0:
        #     print('task_done')
        #     break
        url = q_fetch_info.get(timeout=5)
        print(url)
        try:
            page = req_zhilian(url,status=5)
            job_dict = zhilian_job_info(page)
            list_info = insert_info(job_dict)
            save_info(list_info)
        except Exception as e:
            print('error:',e)
            q_fetch_info.put(url)
        print('save ok')
        time.sleep(1)

def process_fetch_info():
    '''进程：开启 5 个线程抓职位信息'''
    # time.sleep(5)
    print('start crawl')
    threads = []

    t_fetch_url = threading.Thread(target=thread_fetch_url)
    threads.append(t_fetch_url)
    for i in range(5):
        t = threading.Thread(target=thread_fetch_info)
        threads.append(t)


    for t in threads:
        t.start()

    for t in threads:
        t.join()

    print('fetch_info_done')


# def main():
#     '''开始进程'''
#     p1 = multiprocessing.Process(target=process_fetch_url)
#     p2 = multiprocessing.Process(target=process_fetch_info)
#
#     p1.start()
#     p2.start()



if __name__ == '__main__':
    process_fetch_info()
