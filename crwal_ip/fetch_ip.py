#-*- coding:utf-8 -*-
import requests
import bs4
import json
import re
import os
import threading
import time
from implement_dt import Tackle_dt
from crwal_ip import fetch

headers = {
        'User-Agent':'"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) '
                     'AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.2 Safari/534.20",',
}

# 西刺代理
def fetch_xici():
    '''
    download ip from xici website

    '''
    # 连接数据库
    tackle_dt = Tackle_dt()
    url = 'http://www.xicidaili.com/wt'
    page_content = requests.get(url,headers=headers)
    str_content = page_content.text
    soup = bs4.BeautifulSoup(str_content,'lxml')
    # 筛选出所有包含 ip 的 tr 标签
    tr_list = soup.find_all('tr',attrs={'class':['odd','']})
    # 编译 ip 地址正则表达式
    ip_rule = re.compile(r'(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})')
    # 编译 ip 端口正则表达式
    port_rule = re.compile(r'\>(\d+)\<')
    for tr in tr_list:
        str_tr = str(tr)
        re_m = re.search(r'HTTP',str_tr)
        if re_m:
            dic1 = {}
            # 匹配 ip 地址
            ip = re.findall(ip_rule,str_tr)[0]
            # 匹配端口
            port = re.findall(port_rule,str_tr)[0]
            # 组装为可用的 ip 地址
            dic1["http"] = "http://" + ip + ":" + port
            # 验证 ip 是否可用
            if verify_ip(dic1):
                # 验证可用后存入数据库
                tackle_dt.insert_ip(dic1)

# =================================================================================

# 有代理网
def fetch_udaili():
    '''从有代理网下载 IP'''
    # 连接数据库
    tackle_dt = Tackle_dt()
    # 网页请求解析
    url = 'http://www.youdaili.net/Daili/http/29487.html'
    page_content = requests.get(url, headers=headers)
    str_content = page_content.text
    soup = bs4.BeautifulSoup(str_content, 'lxml')
    p_tags = soup.find_all('p')
    # 匹配 IP
    rule = re.compile(r'(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}:\d+)')
    for p in p_tags:
        try:
            ip = re.findall(rule,str(p))[0]
            dic = {}
            if ip:
                dic["http"] = "http://"+ip
                if verify_ip(dic):
                    print(dic)
                    tackle_dt.insert_ip(dic)

        except:
            pass

# =========================================================================
# 66代理

headers1 = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate, sdch',
        'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.6',
        'Connection':'keep-alive',
        'Cookie':'__cfduid=dc82e63a299dce97b98b94d949f5a9bb61484641816;'
                 ' CNZZDATA1253901093=1728273565-1484639487-http%253A%252F%252Fwww.baidu.com%252F%7C1484701785; '
                 'Hm_lvt_1761fabf3c988e7f04bec51acd4073f4=1484646251,1484646378,1484702884,1484703157; '
                 'Hm_lpvt_1761fabf3c988e7f04bec51acd4073f4=1484704429',
        'Host':'www.66ip.cn',
        'Referer':'http://www.66ip.cn/pt.html',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
            }
def fetch_ss():
    tackle_dt = Tackle_dt()
    url = 'http://www.66ip.cn/mo.php?tqsl=50'
    page_content = requests.get(url, headers=headers1)
    str_content = page_content.text
    rule = re.compile(r'(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}:\d+)')
    result = re.findall(rule,str_content)
    for ip in result:
        dic = {}
        dic["http"] = "http://"+ip
        if verify_ip(dic):
            print(dic)
            tackle_dt.insert_ip(dic)


# 首次验证 ip 是否可用
def verify_ip(dic):
    proxies = dic
    fixed_url = 'http://www.baidu.com/'
    try:
        res = requests.get(fixed_url,proxies=proxies,timeout=2)
        # print(res.text)
        if 'STATUS OK' in res.text:
            return True
        else:
            return False
    except:
        return False

# 多线程
funcs = [fetch_xici,fetch_udaili,fetch_ss]
def download_ip():
    print('begin crawling ip')
    threads = []
    for i in range(len(funcs)):
        t = threading.Thread(target=funcs[i])
        threads.append(t)
    for i in range(len(funcs)):
        threads[i].start()
    for i in range(len(funcs)):
        threads[i].join()
    print('finish crawling ip')


download_ip()
# if __name__ == '__main__':
#     while True:
#         print('crawling...')
#         main()
#         print('resting...')
#         # 休息一分钟
#         time.sleep(60)
