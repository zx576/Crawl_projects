#-*- coding:utf-8 -*-
import sqlite3
import os
import json
import re

class Zhilian_url_di():

    def __init__(self):
        # self.name = 'sam'
        self.conn = ''
        self.build_or_connect('zhilian_url.db')

    def build_or_connect(self,database_name):
        
        '''connect a existing sqlite3 database,build one if it doesn't exsits
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
                    URL TEXT NOT NULL,
                    STATUS INTEGER NOT NULL
                );
                ''')

    def insert_zhilian_url(self):
