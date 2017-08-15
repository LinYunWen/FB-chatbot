# -*- coding: utf-8 -*-

import os
import requests
from flask import Flask, request, render_template

import server.information
from server import util
from server.util import ErrorType, InputType, ResponseType, ModeType

import fbmsg.msg_api
from fbmsg.fbmsg import Bot
from database.database import db

app = Flask(__name__)

ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
bot = Bot(ACCESS_TOKEN)

# Init start connection button in dialog
fbmsg.msg_api.set_start_button(ACCESS_TOKEN)
# add to white list
fbmsg.msg_api.add_white_list(ACCESS_TOKEN)
# set messenger extension
fbmsg.msg_api.set_home_url(ACCESS_TOKEN)

# for verify
@app.route('/', methods=['GET'])
def handle_verification():
    if request.args['hub.verify_token'] == os.environ['VERIFY_TOKEN']:
        return request.args['hub.challenge']
    else:
        return 'Wrong Verify Token'

def reply(user_id, mode, info):
    if info['mode'] in ErrorType:
        util.handle_error_request(bot, user_id, info['mode'])
        return 'ok'

    if info['response_type'] == ResponseType.SINGLE:
        bot.reply_generic_template(user_id, mode, info)
    elif info['response_type'] == ResponseType.LIST:
        if info['top_element_style'] == 'compact':
            if info['mode'] == InputType.TRACK or info['mode'] == InputType.ARTIST:
                bot.reply_text(user_id, mode, '抱歉~沒有找到完全相同者\n請問是以下選項嗎？')
                bot.set_sender_action(user_id, 'typing_on')
        bot.reply_list_template(user_id, mode, info)
    util.print_usage(bot, user_id)
    return 'ok'

def process_mode(id, text, mode):
    # for which mode for bot to handle
    # @id: user conversation id
    # @text: the key words will be search
    # @mode: ModeType
    request_token = util.parse_request(text)
    if request_token['mode'] in ErrorType:
        if mode == ModeType.BROADCAST_MODE:
            bot.reply_text(id, mode, text)
        else:
            util.handle_error_request(bot, id, request_token['mode'])
    else:
        info = information.get_info(request_token['token'], request_token['mode'])
        reply(id, mode, info)
    

@app.route('/', methods=['POST'])
def handle_incoming_message():
    data = request.json
    messaging = data['entry'][0]['messaging'][0]
    sender_id = messaging['sender']['id']

    # set action
    bot.set_sender_action(sender_id, 'mark_seen')
    bot.set_sender_action(sender_id, 'typing_on')

    # handle first conversation
    if 'postback' in messaging:
        if messaging['postback']['payload'] == 'first_hand_shack':
            fbmsg.msg_api.first_hand_shack(bot, sender_id)
            return 'ok'

    # request with not pure text message
    if 'attachments' in messaging['message']:
        fbmsg.msg_api.recieve_attachment(bot, sender_id)
        return 'ok'

    # Pure text message
    text = messaging['message']['text']
    print('message: ', text)

    # broadcast mode
    if sender_id == str(os.environ['ADMIN_ID']):
        if text[0] == '!' or text == '！':
            process_mode(sender_id, text[1:], ModeType.BROADCAST_MODE)
            return 'ok'

    # user mode
    process_mode(sender_id, text, ModeType.USER_MODE)

    # set type off
    bot.set_sender_action(sender_id, 'typing_off')
    return 'ok'

@app.route('/index')
def index():
    return render_template('chat_extension/index.html')