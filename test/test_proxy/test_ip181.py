#-*- coding:utf-8 -*-

import logging
import requests
from datetime import datetime
import bs4
import re
from selenium import webdriver
# from .general_methods import save_proxy,req_url
import time
import chardet

logger = logging.getLogger(__name__)

headers_general = {
        'User-Agent':'"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) '
                     'AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.2 Safari/534.20",',
}


def req_url(url, headers, rep_count=1):
    ''' 请求网页，返回 bs 处理过的字符串

    请求过程如果对方拒绝或者状态码不为 200 ，调用 selenium 重新获取 cookie,然后再次请求
    再失败，就直接返回 None

    :param url: 请求地址
    :param headers: 请求头
    :param rep_count: 请求次数，默认为 1，
    :return: bs4 处理过的网页
    '''
    try:
        req = requests.get(url, headers=headers, timeout=2)
        print(req.encoding)
        assert req.status_code == 200
    except Exception as e:

        if rep_count == 1:
            # logging.warning('url：%s 第一次报错，已经跳转重新获取 Cookie,报错信息：%s' %(url,e))
            cookie = get_cookie_by_selenium(url)
            headers['Cookie'] = cookie
            return req_url(url, headers, rep_count=2)
        else:
            logging.warning('url：%s 第二次报错，报错信息：%s' %(url,e))
            return None

    else:
        # soup = bs4.BeautifulSoup(req.text,'lxml')
        return req.text

def get_cookie_by_selenium(url):
    '''使用 selenium 获取 cookie

    :param url: 获取 cookie 的地址
    :return: 返回字符串形式的
    '''
    driver = webdriver.PhantomJS()
    driver.get(url)
    cookie = [item["name"] + "=" + item["value"] for item in driver.get_cookies()]
    cookiestr = ';'.join(item for item in cookie)
    driver.quit()
    return cookiestr


XICI_IP = []
# 西刺代理
def fetch_xici():
    '''从 西刺 网下载 ip'''
    urls = ['http://www.xicidaili.com/wt',
            'http://www.xicidaili.com/nt/',
            'http://www.xicidaili.com/wn/',
            'http://www.xicidaili.com/wt/']
    for url in urls:
        content = req_url(url, headers_general)
        soup = bs4.BeautifulSoup(content, 'lxml')
        if not soup:
            return None
        # 筛选出所有包含 ip 的 tr 标签
        tr_list = soup.find_all('tr', attrs={'class': ['odd', '']})

        for tr in tr_list:
            # try:
                # dct = {}

            soup_td = tr.find_all('td')

            ip = soup_td[1].string
            port = soup_td[2].string

            district = soup_td[3].get_text()
            if district:
                district = district.strip()
            http_type = soup_td[4].string
            http_head = soup_td[5].string

            # dct[http_head] = ip + ':' + port

            if '高匿' in http_type:
                type = 'G'
            elif '透明' in http_type:
                type = 'T'
            else:
                type = 'O'

            # 去重
            if ip in XICI_IP:
                continue
            XICI_IP.append(ip)
            print(ip,port,district,http_head,http_type)

                # save_proxy('西刺', ip, port, http_head, district=district, http_type=type)
            # except Exception as e:
            #     logging.warning('fetch_xici 请求 %s 报错，错误信息：%s' % (url, e))
            #     continue

fetch_xici()
