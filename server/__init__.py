# -*- coding: utf-8 -*-

import os
import requests
from flask import Flask, request

import server.getInfo
from server import util
from server.util import ErrorType, InputType, ResponseType, ModeType
from server import fbmsg
from server.fbmsg import Fbmsg

app = Flask(__name__)

ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
client = Fbmsg(ACCESS_TOKEN)

# Init start connection button in dialog
client.set_start_button()
# add to white list
client.add_white_list()
# set messenger extension
client.set_home_url()

# for verify
@app.route('/', methods=['GET'])
def handle_verification():
    if request.args['hub.verify_token'] == os.environ['VERIFY_TOKEN']:
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

def process_mode(id, text, mode):
    # for which mode for bot to handle
    # @id: user conversation id
    # @text: the key words will be search
    # @mode: ModeType
    request_token = util.parse_request(text)
    if request_token['mode'] in ErrorType:
        if mode == ModeType.BROADCAST_MODE:
            client.reply_text(id, mode, text)
        else:
            util.handle_error_request(client, id, request_token['mode'])
    else:
        info = getInfo.get_info(request_token['token'], request_token['mode'])
        reply(id, mode, info)
    

@app.route('/', methods=['POST'])
def handle_incoming_message():
    data = request.json
    messaging = data['entry'][0]['messaging'][0]
    sender_id = messaging['sender']['id']

    # set action
    client.set_sender_action(sender_id, 'mark_seen')
    client.set_sender_action(sender_id, 'typing_on')

    # handle first conversation
    if 'postback' in messaging:
        if messaging['postback']['payload'] == 'first_hand_shack':
            fbmsg.first_hand_shack(sender_id, client)
            return 'ok'

    # request with not pure text message
    if 'attachments' in messaging['message']:
        fbmsg.recieve_attachment(sender_id, client)
        return 'ok'

    # Pure text message
    text = messaging['message']['text']
    print('message: ', text)

    # broadcast mode
    if sender_id == '1727613570586940':
        if text[0] == '!' or text == '！':
            process_mode(sender_id, text[1:], ModeType.BROADCAST_MODE)
            return 'ok'

    # user mode
    process_mode(sender_id, text, ModeType.USER_MODE)

    # set type off
    client.set_sender_action(sender_id, 'typing_off')
    return 'ok'

