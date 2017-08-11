# -*- coding: utf-8 -*-

import os
import sys, traceback
import requests
from database.database import db

# send
def send(access_token, data):
    response = requests.post('https://graph.facebook.com/v2.6/me/messages?access_token={ACCESS_TOKEN}'.format(ACCESS_TOKEN=access_token), json=data)
    print(response.content)
    return response.content

# broadcast send
def broadcast_send(access_token, data):
    row = db.retrieve_data()
    for row in rows:
        data['recipient']['id'] = row[0]
        send(access_token, data)
    return  reply_text(str(os.environ['ADMIN_ID']), ModeType.USER_MODE, 'finished broadcast sending')