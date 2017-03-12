#-*- coding:utf-8 -*-
import sqlite3
import os
import json
import re

class Tackle_dt():
    ''''''
    def __init__(self):
        self.conn = ''
        self.bulid_or_open('recruiment_info.db')
    def bulid_or_open(self,database_name):

        created = os.path.exists(database_name)
        self.conn = sqlite3.connect(database_name)
        sql_state = '''
                CREATE TABLE Recruitment
                    (
                    ID             INTEGER        PRIMARY KEY,
                    Resource       CHAR(30)       NOT NULL,
                    JobName        TEXT           NOT NULL,
                    Tags           TEXT,
                    Salary         TEXT,
                    RealeaseDate   TEXT           NOT NULL,
                    Experience     TEXT,
                    OfferNum       TEXT,
                    WorkSite       TEXT,
                    JobNature      TEXT,
                    Degree         TEXT,
                    Description    TEXT,
                    Qualification  TEXT,
                    CompanyName    TEXT           NOT NULL,
                    CompanyScale   TEXT,
                    Industry       TEXT,
                    FirmNature     TEXT,
                    FirmWebsite    TEXT,
                    FirmAddr       TEXT,
                    FirmInfo       TEXT,

                    );

        '''

        if not created:
