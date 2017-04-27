import requests
import bs4
import json
import re
import os
import threading
import time
from selenium import webdriver

def req_url(url,headers,rep_count=1):
    ''' 请求网页，返回 bs 处理过的字符串

    请求过程如果对方拒绝或者状态码不为 200 ，调用 selenium 重新获取 cookie,然后再次请求
    再失败，就直接返回 None

    :param url: 请求地址
    :param headers: 请求头
    :param rep_count: 请求次数，默认为 1，
    :return: bs4 处理过的网页
    '''
    try:
        req = requests.get(url,headers=headers,timeout=2)
        # print(req.status_code)
        assert req.status_code == 200
    except Exception as e:
        if rep_count == 1:
            # logging.warning('req_url 第一次报错，已经跳转重新获取 Cookie,报错信息：%s'%e)
            cookie = get_cookie_by_selenium(url)
            print(cookie)
            headers['Cookie'] = cookie
            print(headers)
            return req_url(url,headers,rep_count=2)
        else:
            # logging.warning('req_url 第二次报,返回 None,查看请求逻辑报错信息：%s' %e)
            return None

    else:
        # if req.status_code == 521:
        #     return req_url_521(req.text)
        return req.text


def get_cookie_by_selenium(url):
    '''使用 selenium 获取 cookie

    :param url: 获取 cookie 的地址
    :return: 返回字符串形式的
    '''
    driver = webdriver.PhantomJS()
    driver.get(url)
    # driver.get(url)
    time.sleep(10)
    cookie = [item["name"] + "=" + item["value"] for item in driver.get_cookies()]
    cookiestr = ';'.join(item for item in cookie)
    driver.quit()
    return cookiestr

def req_url_521(url,headers,count=1):

    req = requests.get(url, headers=headers, timeout=2)
    source = req.text
    if req.status_code == 521:
        # 提取其中的JS加密函数
        js_func = ''.join(re.findall(r'(function .*?)</script>', source))
        # 提取其中执行JS函数的参数
        js_arg = ''.join(re.findall(r'setTimeout\(\"(\D+\(\d+\))\"', source))
        # 修改JS函数，使其返回Cookie内容
        js_func = js_func.replace('eval("qo=eval;qo(po);")', 'return po')
        # 执行JS获取Cookie
        js_code = js_func + ';' + 'return ' + js_arg
        driver = webdriver.PhantomJS()
        cookie_str = driver.execute_script(js_code)
        cookie_str = cookie_str.replace("document.cookie='", "")
        cookie = cookie_str.split(';')[0]
        headers['Cookies'] = cookie
        req_url_521(url, headers, count=2)
    else:
        return req.text





headers_general = {
        'User-Agent':'"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) '
                     'AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.2 Safari/534.20",',
}
headers_fp = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Connection': 'keep-alive',
            'Host': 'www.freeproxylists.net',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:50.0) Gecko/20100101 Firefox/50.0',
        }


# 快代理请求头# 快代理请求头
headers_kuai = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate, sdch',
        'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.6',
        'Cache-Control':'max-age=0',
        'Cookie':'sessionid=a76e1c82e71492eba1869a1973610bd6; channelid=0; sid=1491370147849899; _ydclearance=cc9a9863170f0895f520b2e4-c32a-4d36-962f-305f58d952d7-1491385315; Hm_lvt_7ed65b1cc4b810e9fd37959c9bb51b31=1491011473,1491139506,1491187701,1491370620; Hm_lpvt_7ed65b1cc4b810e9fd37959c9bb51b31=1491378119; _ga=GA1.2.511320761.1490863522',
        'Host':'www.kuaidaili.com',
        'Proxy-Connection':'keep-alive',
        'Referer':'https://www.google.com.hk/',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36',
}
# Cookie:
#
def fetch_k1():
    '''下载 快代理 网站IP'''
    urls = ['http://www.kuaidaili.com/free/inha/',
            'http://www.kuaidaili.com/free/intr/',
            'http://www.kuaidaili.com/free/outha/',
            'http://www.kuaidaili.com/free/outtr/']

    KD_IP = []
    for url in urls:

        content = req_url(url,headers_kuai)
        soup = bs4.BeautifulSoup(content,'lxml')

        if not soup:
            return None

        soup_tb = soup.find('tbody')
        soup_tr = soup_tb.find_all('tr')
        for tr in soup_tr:
            try:
                all_td = tr.find_all('td')

                ip        = all_td[0].string
                port      = all_td[1].string
                http_type = all_td[2].string
                http_head = all_td[3].string
                district  = all_td[4].string

                if '高匿' in http_type:
                    type = 'G'
                elif '透明' in http_type:
                    type = 'T'
                else:
                    type = 'O'

                dic = {}
                dic[http_head] = ip + ':' + port

                if dic in KD_IP:
                    continue
                KD_IP.append(dic)

                print(dic,http_type,district)
                # save_proxy(dic,resource='快代理',district=district,http_type=type)
            except Exception as e:
                # logging.warning('fetch_k1 请求 %s 报错，错误信息：%s' % (url, e))
                continue


def freeproxylists():
    url = 'http://www.freeproxylists.net/zh/?page=1'
    content = req_url(url,headers=headers_fp)
    soup = bs4.BeautifulSoup(content,'lxml')
    print(soup.prettify)


# freeproxylists()
fetch_k1()