# -*- coding: utf-8 -*-

import os
import enum
import requests
from database.database import db

class InputType(enum.Enum):
    TRACK = 'track'
    ALBUM = 'album'
    PLAYLIST = 'playlist'
    ARTIST = 'artist'
    INQUERY = 'inquery'

class ResponseType(enum.Enum):
    SINGLE = 'single'
    LIST = 'list'

class ErrorType(enum.Enum):
    BAD_INPUT = 'bad_input'
    NO_RESULT = 'no_result'
    SOMETHING_WRONG = 'something_wrong'

class ModeType(enum.Enum):
    USER_MODE = 'user_mode'
    BROADCAST_MODE = 'broadcast_mode'

def get_summary_total(json):
    # Check if the json has error
    if 'error' in json:
        return 0

    total = int(json['summary']['total'])
    return 4 if total > 4 else total

def get_widget_url(id, input_type):
    return 'https://widget.kkbox.com/v1/?id={ID}&type={INPUT_TYPE}'.format(ID=id, INPUT_TYPE=input_type)

def parse_request(message):
    result = {'mode': ErrorType.BAD_INPUT, 'token': ''}

    if not message or len(message) < 2:
        return result

    # parse mode
    input_type = message[0]
    result['token'] = message[1:]
    if input_type == '/' or input_type == '／':
        result['mode'] = InputType.TRACK
    elif input_type == '#' or input_type == '＃':
        result['mode'] = InputType.ALBUM
    elif input_type == '$' or input_type == '＄':
        result['mode'] = InputType.PLAYLIST
    elif input_type == '@' or input_type == '＠':
        result['mode'] = InputType.ARTIST

    return result

def modify_image_size(url, size):
    index = url.rfind('/')
    if index > 0:
        temp = url[index + 1:]
        expect_size = str(size) + 'x' + str(size) + '.jpg'
        if temp != expect_size:
            return url[0:index + 1] + expect_size
    return url

def artist_songs(id, territory):
    # search for artist's top track
    # @id: artist id
    # @territory: TW, HK, SG, MY, JP 
    headers = {'Authorization': os.environ['AUTHORIZATION']}
    return requests.get('https://api.kkbox.com/v1.1/artists/' + id + '/top-tracks?territory=' + territory + '&limit=3', headers=headers).json()

def search(inquiry, type, territory):
    # search anythings
    # @inquiry: key word for search
    # @type: artist, album, track, playlist
    # @territory: TW, HK, SG, MY, JP 
    payload = {'q': inquiry, 'type': type, 'territory': territory}
    headers = {'Authorization': os.environ['AUTHORIZATION']}

    response = requests.get('https://api.kkbox.com/v1.1/search',params=payload, headers=headers)
    return response.json()

def set_subtitle(type,element):
    if type.value == 'track':
        return '{artist}\n{album}'.format(artist=element['album']['artist']['name'], album=element['album']['name'])
    elif type.value == 'album':
         return element['artist']['name']
    elif type.value == 'playlist':
         return element['description']
    return ' '

def print_usage(bot, user_id):
    if db.get_locale(user_id) == 'zh_TW':
        str = '請輸入\"/歌曲名稱\"\n或輸入\"#專輯名稱\"\n或輸入\"$歌單名稱\"\n或輸入\"@歌手名稱\"'
    else:
        str = 'Please type\"/SONG_NAME\"\nor type\"#ALBUNM_NAME\"\nor type\"$PLAYLIST_NAME\"\nor type\"@ARTIST_NAME\"'
    bot.reply_text(user_id, ModeType.USER_MODE, str)

def handle_error_request(bot, user_id, error_type):
    is_zh = True if db.get_locale(user_id) == 'zh_TW' else False
    if error_type == ErrorType.BAD_INPUT:
        str = '未設定之指令' if is_zh else 'Not set command!'
        bot.reply_text(user_id, ModeType.USER_MODE, str)
        print_usage(bot, user_id)
    elif error_type == ErrorType.NO_RESULT:
        str = '抱歉～沒有尋找到任何資料' if is_zh else 'Sorry~ no any result for searching!'
        bot.reply_text(user_id, ModeType.USER_MODE, str)
    elif error_type == ErrorType.SOMETHING_WRONG:
        str = '抱歉～有錯誤' if is_zh else 'Sorry~ something wrong!'
        bot.reply_text(user_id, ModeType.USER_MODE, str)
    return 0