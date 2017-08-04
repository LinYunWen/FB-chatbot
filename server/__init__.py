# -*- coding: utf-8 -*-

import os
import sys, traceback
import requests
import psycopg2
# from urllib.parse import urlparse
import urllib.parse
from flask import Flask, request
from pymessenger.bot import Bot

from server import util
from server.util import ErrorType, InputType, ResponseType
from server.fbmsg import Fbmsg

app = Flask(__name__)

# connect to database
urllib.parse.uses_netloc.append('postgres')
url = urllib.parse.urlparse(os.environ['DATABASE_URL'])
conn = psycopg2.connect(
    database = url.path[1:],
    user = url.username,
    password = url.password,
    host = url.hostname,
    port = url.port
)
cur = conn.cursor()

# this is a token to match FB fans page
# Light up
# ACCESS_TOKEN = 'EAAEtsX9w5Q0BAHz42VnrkeSNajWpvJjc8ONCs4plPKlBzoafvDTxTEkVY1gGmTxiDcPKauUVHmACxSoyJ715dwhuvRV78QZCWKrQNnACFevghRzjU33xWYFuwZChpDTsVpnSZCtKmZBayMzOzXFdiWly9OZAJPgjgptYzBZAnivwZDZD'
# test bot
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
bot = Bot(ACCESS_TOKEN)
client = Fbmsg(ACCESS_TOKEN)
# Init start connection button in dialog
client.set_start_button()

is_match = False
counter = 0

# for verify
@app.route('/', methods=['GET'])
def handle_verification():
    if request.args['hub.verify_token'] == 'test_for_verify':
        return request.args['hub.challenge']
    else:
        return 'Wrong Verify Token'

def get_access_token():
    return 0

def handle_error_request(user_id, error_type):
    global counter
    if error_type == ErrorType.BAD_INPUT:
        client.reply_text(user_id, '未設定之指令')
        client.reply_text(user_id, '請輸入\"/歌曲名稱\"\n或輸入\"#專輯名稱\"\n或輸入\"$歌單名稱\"\n或輸入\"@歌手名稱\"')
        #counter = (counter + 1) % 3
        #print('counter: ', counter)
    elif error_type == ErrorType.NO_RESULT:
        client.reply_text(user_id, '抱歉～沒有尋找到任何資料')
    elif error_type == ErrorType.SOMETHING_WRONG:
        client.reply_text(user_id, '抱歉～有錯誤')

    return 0

def matching_result(input, expect):
    global is_match
    is_match = False

    index = expect.find('(')
    if index >= 0:
        if index >= 2:
            expect_pre = expect[:index-1]
            is_match = True if input.lower() == expect_pre.lower() else False
    else:
        is_match = True if input.lower() == expect.lower() else False
    return is_match


def get_info(msg, info_type):
    global is_match
    get = {
        InputType.TRACK: _get_track,
        InputType.ALBUM: _get_album,
        InputType.PLAYLIST: _get_playlist,
        InputType.ARTIST: _get_artist,
    }
    is_match = False

    try:
        info = get[info_type](msg)
    except:
        tb = sys.exc_info()
        print(tb[1])
        print(traceback.print_tb(tb[2]))
        return {'mode':ErrorType.SOMETHING_WRONG}
    return info

def set_subtitle(type,element):
    if type.value == 'track':
        return '{artist}\n{album}'.format(artist=element['album']['artist']['name'], album=element['album']['name'])
    elif type.value == 'album':
         return element['artist']['name']
    elif type.value == 'playlist':
         return element['description']
    return ' '

def _get_reply(msg, type, id):
    if type.value == 'track' and id != 'none':
        search_result = util.artist_songs(id, 'TW')
    else:
        search_result = util.search(msg, type.value, 'TW')
    total = util.get_summary_total(search_result)

    if not total:
        return {'mode': ErrorType.NO_RESULT}

    data = []
    match = None
    for d in search_result[type.value + 's']['data'] if id == 'none' else search_result['data']:
        # set title and subtitle
        title = d['name'] if 'name' in d else d['title']
        subtitle = set_subtitle(type,d)
        
        pk = d['id']
        widget_url = util.get_widget_url(pk, type.value if type.value != 'track' else 'song')

        data.append({
            'title': title,
            'subtitle': subtitle,
            'widget_song_url': widget_url,
            'widget_image_url': d['images'][-1]['url'] if 'images' in d else d['album']['images'][-1]['url'],
            'web_url': d['url']
        })

        # XXX: WTF? what does this if stmt do?
        if id == 'none' and not is_match and matching_result(msg, title):
            match = data[-1]
            if type.value == 'artist':
                return {'id':pk, 'data':match}

    # Replace 1st item to match data
    if id == 'none' and is_match and match:
        data.remove(match)
        data.insert(0, match)

    return {
        'mode': type,
        'response_type': ResponseType.SINGLE if is_match or len(data) < 2 else ResponseType.LIST,
        'top_element_style': 'compact' if id == 'none' else 'large',
        'data': data,
        'token': msg,
    }

def _get_album(msg):
    return _get_reply(msg, InputType.ALBUM, 'none')

def _get_playlist(msg):
    return _get_reply(msg, InputType.PLAYLIST, 'none')

def _get_artist(msg):
    global is_match
    data = _get_reply(msg, InputType.ARTIST, 'none')
    if is_match:
        id = data['id']
        artist_data = data['data']
        is_match = False
        track_data = _get_reply(msg, InputType.TRACK, id)
        track_data['data'].insert(0, artist_data)
        data = track_data
    return data
    


def _get_track(msg):
    return _get_reply(msg, InputType.TRACK, 'none')

def reply(user_id, info):
    if info['mode'] in ErrorType:
        handle_error_request(user_id, info['mode'])
        return 'ok'

    if info['response_type'] == ResponseType.SINGLE:
        client.reply_generic_template(user_id, info)
    elif info['response_type'] == ResponseType.LIST:
        if info['top_element_style'] == 'compact':
            if info['mode'] == InputType.TRACK or info['mode'] == InputType.ARTIST:
                client.reply_text(user_id, '抱歉~沒有找到完全相同者\n請問是以下選項嗎？')
                client.set_sender_action(user_id, 'typing_on')
        client.reply_list_template(user_id, info)
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
            client.reply_text(sender_id, '請輸入\"/歌曲名稱\"\n或輸入\"#專輯名稱\"\n或輸入\"$歌單名稱\"\n或輸入\"@歌手名稱\"')
            client.set_sender_action(sender_id, 'typing_off')
            print(data)
            cur.execute('INSERT INTO audience (id, user_id, first_name, last_name, profile_pic, locale, timezone, gender) VALUES (1, ' + sender_id + ', "Hello", "你好", "fjkdlsul", "en-US", 8, "male")')
            conn.commit()
            return 'ok'

    # request with not pure text message
    if 'attachments' in messaging['message']:
        client.reply_text(sender_id, '❤️')
        client.reply_text(sender_id, '😁')
        client.set_sender_action(sender_id, 'typing_off')
        return 'ok'

    # Pure text message
    text = messaging['message']['text']
    print('message: ', text)
    request_token = util.parse_request(text)
    if request_token['mode'] in ErrorType:
        handle_error_request(sender_id, request_token['mode'])
    else:
        info = get_info(request_token['token'], request_token['mode'])
        reply(sender_id, info)

    # set type off
    client.set_sender_action(sender_id, 'typing_off')
    return 'ok'

