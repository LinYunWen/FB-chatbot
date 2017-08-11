# -*- coding: utf-8 -*-

import sys, traceback
import requests
from server.util import ModeType

def first_hand_shack(id, bot):
    # for users first using the bot, will get their user profile data
    # @id: user conversation id
    # @bot: Fbmsg object
    bot.reply_text(id, ModeType.USER_MODE, '請輸入\"/歌曲名稱\"\n或輸入\"#專輯名稱\"\n或輸入\"$歌單名稱\"\n或輸入\"@歌手名稱\"')
    bot.set_sender_action(id, 'typing_off')
    try:
        dict = get_user_info(bot.access_token, id)
        # db.insert_new_row(id, dict)
    except:
        tb = sys.exc_info()
        print(tb[1])
        print(traceback.print_tb(tb[2]))
    return dict

def recieve_attachment(id, bot):
    # becouse of just accept text message input, discarding not text message
    # @id: user conversation id
    # @bot: Fbmsg object
    bot.reply_text(id, ModeType.USER_MODE, '❤️')
    bot.reply_text(id, ModeType.USER_MODE, '😁')
    bot.set_sender_action(id, 'typing_off')
    return 

# set messenger profile 
def set_start_button(access_token):
    data = {
        'get_started': {
            'payload': 'first_hand_shack'
        }
    }
    response = requests.post('https://graph.facebook.com/v2.6/me/messenger_profile?access_token={ACCESS_TOKEN}'.format(ACCESS_TOKEN=access_token), json=data)
    return response.content

def add_white_list(access_token):
    data = {
        'whitelisted_domains': [
            'https://dry-forest-96464.herokuapp.com/',
            'https://arcane-chamber-93170.herokuapp.com/'
        ]
    }
    response = requests.post('https://graph.facebook.com/v2.6/me/messenger_profile?access_token={ACCESS_TOKEN}'.format(ACCESS_TOKEN=access_token))
    print('white list: ', response.content)
    return response.content

def set_home_url(access_token):
    data = {
        'home_url' : {
            'url': 'https://dry-forest-96464.herokuapp.com/index',
            'webview_height_ratio': 'tall',
            'in_test': True
        }
    }
    response = requests.post('https://graph.facebook.com/v2.6/me/messenger_profile?access_token={ACCESS_TOKEN}'.format(ACCESS_TOKEN=access_token))
    print('home url: ', response.content)
    return response.content

def get_user_info(access_token, id):
    return requests.get('https://graph.facebook.com/v2.6/{USER_ID}?fields=first_name,last_name,profile_pic,locale,timezone,gender&access_token={ACCESS_TOKEN}'.format(USER_ID=id, ACCESS_TOKEN=access_token)).json()