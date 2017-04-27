from selenium import webdriver
import requests
import re

url = 'http://www.kuaidaili.com/free/inha/'
url2 = 'http://www.baidu.com'
url3 = 'http://www.freeproxylists.net/zh/?page=1'
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
driver = webdriver.PhantomJS()
driver.get(url3)
print(driver.page_source)
# js = "'identityCookie' => ['name' => '_identity-frontend', 'httpOnly' => false]"
# driver.execute_script(js)
# cookie = driver.execute_script('document.cookie')
# body = driver.page_source
# js_func = ''.join(re.findall(r'(function .*?)</script>', body))
# print(js_func)
# 提取其中执行JS函数的参数
# js_arg = ''.join(re.findall(r'setTimeout\(\"\D+\((\d+)\)\"', body))
# print(js_arg)
# 修改JS函数，使其返回Cookie内容
# js_func = js_func.replace('eval("qo=eval;qo(po);")', 'return po')
# print(js_func)
# 执行JS获取Cookie
# cookie_str = driver.execute_script(js_func, js_arg)
# print(cookie_str)/

# sses = requests.session()
# req = sses.get(url)
# print(req.text)
