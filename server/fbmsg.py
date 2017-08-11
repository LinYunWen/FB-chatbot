# -*- coding: utf-8 -*-

import os
import sys, traceback
import requests
from server.connectDB import db
from server.util import ErrorType, InputType, ResponseType, ModeType

class Fbmsg(object):
    def __init__(self, access_token):
        self.access_token = access_token

    # send
    def send(self, data):
        response = requests.post('https://graph.facebook.com/v2.6/me/messages?access_token={ACCESS_TOKEN}'.format(ACCESS_TOKEN=self.access_token), json=data)
        print(response.content)
        return response.content

    # broadcast send
    def broadcast_send(self, data):
        row = db.retrieve_data()
        for row in rows:
            data['recipient']['id'] = row[0]
            self.send(data)
        return  self.reply_text('1727613570586940', ModeType.USER_MODE, 'finished broadcast sending')

    def produce_item(self, data, type):
        if type == InputType.TRACK:
            webview_type = 'compact'
        elif type == InputType.ALBUM or type == InputType.PLAYLIST:
            webview_type = 'tall'
        elif type == InputType.ARTIST:
            webview_type = 'full'

        item = {
            'title': data['title'],
            'subtitle': data['subtitle'],
            'image_url': data['widget_image_url'],
            'default_action': {
                'type': 'web_url',
                'url': data['widget_song_url'] if type != InputType.ARTIST else data['web_url'],
                'webview_height_ratio': webview_type
            }
        }
        return item

    def produce_elements(self, info):
        elements = []

        print('data length:', len(info['data']))
        if info['response_type'] == ResponseType.SINGLE:
            for i in range(0, len(info['data']) if len(info['data']) <= 10 else 10):
                item = self.produce_item(info['data'][i], info['mode'])
                item['buttons'] = self.produce_buttons(info, i)
                elements.append(item)
        else:
            if info['top_element_style'] == 'large':
                item = self.produce_item(info['data'][0], InputType.ARTIST)
                elements = [item]
                for i in range(1, len(info['data']) if len(info['data']) <= 4 else 4):
                    item = self.produce_item(info['data'][i], info['mode'])
                    elements.append(item)
            else:
                for i in range(0, len(info['data']) if len(info['data']) <= 4 else 4):
                    item = self.produce_item(info['data'][i], info['mode'])
                    elements.append(item)
        return elements

    def produce_buttons(self, info, index):
        buttons = [{
            'type': 'web_url',
            'url': info['data'][index]['web_url'],
            'title': 'Web page'
        }]

        if info['response_type'] == ResponseType.SINGLE:
            buttons.insert(0, {'type': 'element_share'})
        else:
            if info['top_element_style'] == 'compact':
                buttons[0]['url'] = 'https://www.kkbox.com/tw/tc/search.php?word={token}'.format(token=info['token'])
                buttons[0]['title'] = 'More'
        return buttons

    # reply request
    def reply_text(self, user_id, mode, message):
        data = {
            'recipient': {'id': user_id},
            'message': {'text': message}
        }
        return self.send(data) if mode == ModeType.USER_MODE else self.broadcast_send(data)

    def reply_greeting_message(self):
        data = {
            'setting_type': 'greeting',
            'greeting': {
                'text': '請輸入\"/歌曲名稱\"\n或輸入\"#專輯名稱\"\n或輸入\"$歌單名稱\"\n或輸入\"@歌手名稱\"'
            }
        }

    def reply_image_url(self, user_id, mode, image_url):
        data = {
            'recipient': {
                'id': user_id
            },
            'message': {
                'attachment': {
                    'type': 'image',
                    'payload': {
                        'url': image_url
                    }
                }
            }
        }
        return self.send(data) if mode == ModeType.USER_MODE else self.broadcast_send(data)

    def reply_generic_template(self, user_id, mode, info):
        element = self.produce_elements(info)
        data = {
            'recipient': {
                'id': user_id
            },
            'message': {
                'attachment': {
                    'type': 'template',
                    'payload': {
                        'template_type': 'generic',
                        'sharable': True,
                        'image_aspect_ratio': 'square',
                        'elements': element
                    }
                }
            }
        }
        return self.send(data) if mode == ModeType.USER_MODE else self.broadcast_send(data)

    def reply_list_template(self, user_id, mode, info):
        elements = self.produce_elements(info)
        buttons = self.produce_buttons(info, 0)

        data = {
            'recipient': {
                'id': user_id
            },
            'message': {
                'attachment': {
                    'type': 'template',
                    'payload': {
                        'template_type': 'list',
                        'top_element_style': info['top_element_style'],
                        'elements': elements,
                        'buttons': buttons
                    }
                }
            }
        }
        return self.send(data) if mode == ModeType.USER_MODE else self.broadcast_send(data)

    # set messenger profile 
    def set_start_button(self):
        data = {
            'get_started': {
                'payload': 'first_hand_shack'
            }
        }
        response = requests.post('https://graph.facebook.com/v2.6/me/messenger_profile?access_token={ACCESS_TOKEN}'.format(ACCESS_TOKEN=self.access_token), json=data)
        return response.content

    def add_white_list(self):
        data = {
            'whitelisted_domains': [
                'https://dry-forest-96464.herokuapp.com/',
                'https://arcane-chamber-93170.herokuapp.com/'
            ]
        }
        response = requests.post('https://graph.facebook.com/v2.6/me/messenger_profile?access_token={ACCESS_TOKEN}'.format(ACCESS_TOKEN=self.access_token))
        print('white list: ', response.content)
        return response.content

    def set_home_url(self):
        data = {
            'home_url' : {
                'url': 'https://dry-forest-96464.herokuapp.com/index',
                'webview_height_ratio': 'tall',
                'in_test': True
            }
        }
        response = requests.post('https://graph.facebook.com/v2.6/me/messenger_profile?access_token={ACCESS_TOKEN}'.format(ACCESS_TOKEN=self.access_token))
        print('home url: ', response.content)
        return response.content

    def set_sender_action(self, user_id, action):
        data = {
            'recipient': {
                'id': user_id
            },
            'sender_action': action
        }
        return self.send(data)

    def get_user_info(self, id):
        return requests.get('https://graph.facebook.com/v2.6/{USER_ID}?fields=first_name,last_name,profile_pic,locale,timezone,gender&access_token={ACCESS_TOKEN}'.format(USER_ID=id, ACCESS_TOKEN=self.access_token)).json()

def first_hand_shack(id, bot):
    # for users first using the bot, will get their user profile data
    # @id: user conversation id
    # @bot: Fbmsg object
    bot.reply_text(id, ModeType.USER_MODE, '請輸入\"/歌曲名稱\"\n或輸入\"#專輯名稱\"\n或輸入\"$歌單名稱\"\n或輸入\"@歌手名稱\"')
    bot.set_sender_action(id, 'typing_off')
    try:
        dict = bot.get_user_info(id)
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