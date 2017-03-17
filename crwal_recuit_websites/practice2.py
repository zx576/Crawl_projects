#-*- coding:utf-8 -*-
import re
import pickle
import requests
# ss = '''
# fdsfsfsf,
# fas'fds'f
# '''
#
# ss = ss.replace('f','x')
# print(ss)
#
# ss = pickle.dumps(ss)
#
# print(ss)
#
# dd = pickle.loads(ss)
#
# print(dd)

url = 'http://www.baidu.com'
req = requests.get(url)
print(req)

print(type(req))
# print(str(req)[-5:-2])
print(req.status_code)
print(type(req.status_code))
