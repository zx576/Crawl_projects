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
                        ID INTEGER PRIMARY KEY  NOT NULL,
                        STATUS         INTEGER NOT NULL,
                        Resource       TEXT,
                        JobName        TEXT,
                        Tags           TEXT,
                        Salary         TEXT,
                        RealeaseDate   TEXT,
                        Experience     TEXT,
                        OfferNum       TEXT,
                        WorkSite       TEXT,
                        JobNature      TEXT,
                        Degree         TEXT,
                        Description    TEXT,
                        Qualification  TEXT,
                        CompanyName    TEXT,
                        CompanyScale   TEXT,
                        Industry       TEXT,
                        FirmNature     TEXT,
                        FirmWebsite    TEXT,
                        FirmAddr       TEXT,
                        FirmInfo       TEXT
                    );
                    '''
        if not created:
            self.conn.execute(sql_state)
            print('ok')

    def insert_info(self,info):
        sql = r'''
                INSERT INTO Recruitment(ID,STATUS,Resource,JobName,Tags,Salary,RealeaseDate,Experience,
                                    OfferNum,WorkSite,JobNature,Degree,Description,Qualification,
                                    CompanyName,CompanyScale,Industry,FirmNature,FirmWebsite,
                                    FirmAddr,FirmInfo)
                VALUES(NULL,1,"%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s",
                            "%s","%s","%s","%s","%s","%s","%s")
               '''%(info[0],info[1],info[2],info[3],info[4],info[5],info[6],info[7],info[8],info[9],info[10],info[11],info[12],info[13],info[14],info[15],info[16],info[17],info[18])
        self.conn.execute(sql)
        self.conn.commit()


    def show_all(self):
        sql = r'SELECT * FROM Recruitment WHERE id = 12'
        query = self.conn.execute(sql)
        print(query.fetchall())

    def inspect_info(self,info):
        sql = 'SELECT * FROM WHERE JobName ="%s" AND CompanyName = "%s"'%(info[1],info[12])
        query = self.conn.execute(sql)
        if len(query) > 0:
            return False
        else:
            return True








td = Tackle_dt()
td.show_all()


















        #############################################
