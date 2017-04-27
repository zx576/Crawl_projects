import requests
import bs4

url = 'http://www.kuaidaili.com/free/inha/'
headers = {

        'Cookie':'_ydclearance=dcf0595b71b7ae8b25c33386-f032-405c-87d6-8cdb80e9b51b-1490870715; sessionid=7eb2f2abb2c1aa07f4425340c99f3573; channelid=0; sid=1490863229901572; _ga=GA1.2.511320761.1490863522; Hm_lvt_7ed65b1cc4b810e9fd37959c9bb51b31=1490863522; Hm_lpvt_7ed65b1cc4b810e9fd37959c9bb51b31=1490864591',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36'
}


def fetch_k1():
    urls = ['http://www.kuaidaili.com/free/inha/','http://www.kuaidaili.com/free/intr/','http://www.kuaidaili.com/free/outha/','http://www.kuaidaili.com/free/outtr/']
    for url in urls:
        req = requests.get(url,headers=headers)
        page = req.text
        soup = bs4.BeautifulSoup(page,'lxml')
        soup_tb = soup.find('tbody')
        soup_tr = soup_tb.find_all('tr')
        for tr in soup_tr:
            ip = tr.find('td',attrs={'data-title':'IP'}).string
            port = tr.find('td',attrs={'data-title':'PORT'}).string
            type = tr.find('td',attrs={'data-title':'类型'}).string
            proxy = ip + ':' + port
            dic = {}
            dic[type] = proxy
            print(dic)




fetch_k1()
