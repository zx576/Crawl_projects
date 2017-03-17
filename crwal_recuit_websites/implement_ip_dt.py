#-*- coding:utf-8 -*-
import sqlite3
import os
import json
import re

class Tackle_dt:

    '''
    封装了爬取 IP 的一些数据库操作

    初始化
    a = Tackle_dt()
    查看数据库中还剩多少有效数据
    a.check_database()
    检测数据是否已经存在,返回布尔值
    a.inspect_ip('http://123.234.547.34:8081')
    存入 IP
    a.insert_ip('http://123.234.547.34:8081')
    删除 IP，接受单个或多个索引值
    a.delete_ip(id=1)
    a.delete_ip(id=[1,2,3,4])
    提取最新的一个 ip
    a.extract_one_ip()
    以 list 形式返回 n 个可用 IP，如果数据库数据量小于 N，则返回当前所有数据
    a.extract_n_ip(3)

    '''
    def __init__(self):

        self.conn = ''
        self.build_or_connect('iplist.db')

    def build_or_connect(self,database_name):
        '''
        function:connect a existing sqlite3 database,build one if it doesn't exsits
        >>>build_or_connect('iplist.db')
        >>><sqlite3.Connection object at 0x0000000000818650>
        '''
        created = os.path.exists(database_name)
        self.conn = sqlite3.connect(database_name)

        if not created:
            self.conn.execute('''
                CREATE TABLE IPLIST
                (
                    ID INTEGER PRIMARY KEY,
                    IP CHAR(30) NOT NULL,
                    STATUS INTEGER NOT NULL
                );
                ''')


    def inspect_ip(self,ip):

        '''check whether there was already a dupicate ip address'''

        sql = r'SELECT * FROM IPLIST WHERE IP = "%s";'%ip
        res = ''
        try:
            query = self.conn.execute(sql)
            res = query.fetchall()
        except Exception as e:
            print(e)
        if len(res) == 0:
            print('ok')
            return True

    def insert_ip(self,ip):

        '''insert into a new ip addr'''

        sql = r'''
                INSERT INTO IPLIST(ID,IP,STATUS)
                VALUES(NULL,"%s",1)
               '''%(ip)
        if self.inspect_ip(ip):
            self.conn.execute(sql)
            self.conn.commit()
            print('insert_ip ok')


    def delete_ip(self,id):

        '''change the invalid ip status'''

        # delete_ip_list = []
        sql = 'UPDATE IPLIST set STATUS = 2 WHERE ID=%d;'
        if isinstance(id,list):
            for i in id:
                exce_sql = sql%i
                self.conn.execute(exce_sql)
                print('delete ok')
        else:
            self.conn.execute(sql%(id))

        self.conn.commit()
        print('delete ok')



    def _extract_one_ip(self):

        '''返回从数据库中抽出的一组最新数据，不开放给外界使用'''

        sql = r'SELECT max(id) FROM IPLIST WHERE STATUS = 1'
        last_id = self.conn.execute(sql).fetchone()[0]
        print(last_id)
        sql2 = r'SELECT * FROM IPLIST WHERE ID = %d;'%last_id
        lastest_ip = self.conn.execute(sql2).fetchone()
        # print(lastest_ip)
        return lastest_ip

    def extract_one_ip(self):

        '''对数据库中返回的数据进行处理，做成对外的接口'''

        latest_ip = self._extract_one_ip()
        str_ip = re.sub('\'', '\"', latest_ip[1])
        dict_ip = json.loads(str_ip)
        self.delete_ip(latest_ip[0])
        return dict_ip

    def _extract_n_ip(self,n):

        '''extract n ip,if there is not enough,return all ip'''

        sql = r'SELECT id FROM IPLIST WHERE STATUS = 1'
        query = self.conn.execute(sql)
        all_id = query.fetchall()
        all_id_unpack = []
        for id in all_id:
            all_id_unpack.append(id[0])
        # print(all_id_unpack)
        all_id_r = all_id_unpack[::-1]
        sql2 = r'SELECT * FROM IPLIST WHERE ID = %d;'
        n_ip = []
        if len(all_id_r) < n:
            n = len(all_id_r)
        for id in all_id_r[:n]:
            e_sql = sql2%id
            one_ip = self.conn.execute(e_sql).fetchone()
            n_ip.append(one_ip)
        # print(n_ip)
        return n_ip

    def extract_n_ip(self,n):

        '''返回 n 个 IP 数据，打包为 list ,供外界调用'''

        n_ip = self._extract_n_ip(n)
        ip_list = []
        delete_id_list = []
        for ip in n_ip:
            # str_ip = ip[1]
            str_ip = re.sub('\'', '\"', ip[1])
            dct_ip = json.loads(str_ip)
            ip_list.append(dct_ip)
            delete_id_list.append(ip[0])
        self.delete_ip(delete_id_list)
        return ip_list

    def check_database(self):
        sql = r'SELECT id FROM IPLIST WHERE STATUS = 1'
        query = self.conn.execute(sql)
        all_id = query.fetchall()
        return len(all_id)


a = Tackle_dt()
# print(a.extract_one_ip())
print(a.check_database())
