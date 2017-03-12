#-*- coding:utf-8 -*-
# import re
# a = ''' 职位描述：  1、游戏服务器后端逻辑的开发和维护；  2、基
# 		于MySQL/MongoDB的数据库开发和维护；  3、按照项目计划，按时提交高质量的代码，完成
# 		开发任务；  4、积极参与工作相关技术的研究；     任职资格：  1、大专以上学历，两
# 		年以上开发经验，一年以上Python开...
#         '''
#
#
# rule = re.compile(r'\w+(?=：)')
#
# res = re.findall(rule,a)
#
# print(res)
import sqlite3

sql = '''
    CREATE TABLE TEST
        (
        ID INTEGER PRIMARY KEY,
        测试中文 CHAR(30) NOT NULL
        );
'''
conn = sqlite3.connect('text.db')
# conn.execute(sql)
# conn.commit()
# conn.close()

sql2 = '''
    INSERT INTO TEST(ID,测试中文)
    VALUES(NULL,"%s")
'''%('测试插入')

conn.execute(sql2)

conn.commit()
conn.close()
print('ok')
