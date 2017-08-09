# -*- coding: utf-8 -*-

import os
import psycopg2
import urllib.parse

class ConnectDB:
    cur = None
    conn = None

    # connect to database
    # def connect_database(self):
    def __init__(self):
        urllib.parse.uses_netloc.append('postgres')
        url = urllib.parse.urlparse(os.environ['DATABASE_URL'])
        self.conn = psycopg2.connect(
            database = url.path[1:],
            user = url.username,
            password = url.password,
            host = url.hostname,
            port = url.port
        )
        self.cur = self.conn.cursor()

    def insert_new_row(self, id, dict):
        self.cur.execute("INSERT INTO audience (user_id, first_name, last_name, profile_pic, locale, timezone, gender) VALUES ('%s', '%s', '%s', '%s', '%s', %d, '%s')" % (id, dict['first_name'], dict['last_name'], dict['profile_pic'], dict['locale'], dict['timezone'], dict['gender']))
        self.conn.commit()
    
    def retrieve_data(self):
        cur.execute('SELECT user_id from audience')
        rows = cur.fetchall()
        return rows

db = ConnectDB()
