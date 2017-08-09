# -*- coding: utf-8 -*-

import os
import sys, traceback
import requests
from flask import Flask, request

import server.getInfo
from server.connectDB import db
from server import util
from server.util import ErrorType, InputType, ResponseType, ModeType
from server import fbmsg
from server.fbmsg import Fbmsg

app = Flask(__name__)

ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
client = Fbmsg(ACCESS_TOKEN)
# Init start connection button in dialog
client.set_start_button()

# for verify
@app.route('/', methods=['GET'])
def handle_verification():
    if request.args['hub.verify_token'] == 'test_for_verify':
        return request.args['hub.challenge']
    else:
        return 'Wrong Verify Token'

def reply(user_id, mode, info):
    if info['mode'] in ErrorType:
        util.handle_error_request(client, user_id, info['mode'])
        return 'ok'

    if info['response_type'] == ResponseType.SINGLE:
        client.reply_generic_template(user_id, mode, info)
    elif info['response_type'] == ResponseType.LIST:
        if info['top_element_style'] == 'compact':
            if info['mode'] == InputType.TRACK or info['mode'] == InputType.ARTIST:
                client.reply_text(user_id, mode, '抱歉~沒有找到完全相同者\n請問是以下選項嗎？')
                client.set_sender_action(user_id, 'typing_on')
        client.reply_list_template(user_id, mode, info)
    return 'ok'

@app.route('/', methods=['POST'])
def handle_incoming_message():
    data = request.json
    messaging = data['entry'][0]['messaging'][0]
    sender_id = messaging['sender']['id']

    # set action
    client.set_sender_action(sender_id, 'mark_seen')
    client.set_sender_action(sender_id, 'typing_on')
    #print(data)

    # handle first conversation
    if 'postback' in messaging:
        if messaging['postback']['payload'] == 'first_hand_shack':
            client.reply_text(sender_id, ModeType.USER_MODE, '請輸入\"/歌曲名稱\"\n或輸入\"#專輯名稱\"\n或輸入\"$歌單名稱\"\n或輸入\"@歌手名稱\"')
            client.set_sender_action(sender_id, 'typing_off')
            try:
                fbmsg.cur.execute("INSERT INTO audience (user_id, first_name, last_name, profile_pic, locale, timezone, gender) VALUES (" + sender_id + ", '---', '---', '---', '---', 8, '---')")
                fbmsg.conn.commit()
            except:
                tb = sys.exc_info()
                print(tb[1])
                return 'ok'
            return 'ok'

    # request with not pure text message
    if 'attachments' in messaging['message']:
        client.reply_text(sender_id, ModeType.USER_MODE, '❤️')
        client.reply_text(sender_id, ModeType.USER_MODE, '😁')
        client.set_sender_action(sender_id, 'typing_off')
        return 'ok'

    # Pure text message
    text = messaging['message']['text']
    print('message: ', text)

    # broadcast mode
    if sender_id == '1727613570586940':
        if text[0] == '!' or text == '！':
            request_token = util.parse_request(text[1:])
            if request_token['mode'] in ErrorType:
                client.reply_text(sender_id, ModeType.BROADCAST_MODE, text[1:])
            else:
                info = getinfo.get_info(request_token['token'], request_token['mode'])
                reply(sender_id, ModeType.BROADCAST_MODE, info)
            return 'ok'

    # user mode
    request_token = util.parse_request(text)
    if request_token['mode'] in ErrorType:
        util.handle_error_request(client, sender_id, request_token['mode'])
    else:
        info = getInfo.get_info(request_token['token'], request_token['mode'])
        reply(sender_id, ModeType.USER_MODE, info)

    # set type off
    client.set_sender_action(sender_id, 'typing_off')
    return 'ok'

