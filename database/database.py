# -*- coding: utf-8 -*-

import os
import psycopg2
import urllib.parse

class Database:
    cur = None
    conn = None

    # connect to database
    def __init__(self, database_url):
        urllib.parse.uses_netloc.append('postgres')
        url = urllib.parse.urlparse(database_url)
        self.conn = psycopg2.connect(
            database = url.path[1:],
            user = url.username,
            password = url.password,
            host = url.hostname,
            port = url.port
        )
        self.cur = self.conn.cursor()

    def insert_new_row(self, id, dict):
        # insert the user data to DB
        # @id: user conversation id
        # @dict: the user data FB defined
        self.cur.execute("INSERT INTO audience (user_id, first_name, last_name, profile_pic, locale, timezone, gender) VALUES ('%s', '%s', '%s', '%s', '%s', %d, '%s')" % (id, dict['first_name'], dict['last_name'], dict['profile_pic'], dict['locale'], dict['timezone'], dict['gender']))
        self.conn.commit()
    
    def retrieve_data(self):
        # retrieve the user data from DB
        cur.execute('SELECT user_id from audience')
        rows = cur.fetchall()
        return rows

    def get_locale(self, user_id):
        try:
            self.cur.execute("SELECT locale FROM audience WHERE user_id='{id}';".format(id=user_id))
            rows = self.cur.fetchall()
        except:
            print('no this user_id')
            return False
        return rows[0][0]

db = Database(os.environ['DATABASE_URL'])
