#-*- coding:utf-8 -*-
import requests

def verify_ip(dic):
    proxies = dic
    fixed_url = 'http://www.baidu.com/'
    try:
        res = requests.get(fixed_url,proxies=proxies,timeout=1)
    except:
        return False
    else:
        if res.status_code == 200:
            return True
        else:
            return False


dic = {"http": "http://1.180.239.133:9999"}

print(verify_ip(dic))
