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
        response = requests.post('https://graph.facebook.com/v2.6/me/messages?access_token=' + self.access_token, json=data)
        print(response.content)
        return response.content

    def broadcast_send(se１lf, data):
        row = db.retrieve_data()
        for row in rows:
            data['recipient']['id'] = row[0]
            self.send(data)
        return  self.reply_text('1727613570586940', ModeType.USER_MODE, 'finished broadcast sending')

    def produce_elements(self, info):
        elements = []
        if info['mode'] == InputType.TRACK:
            webview_type = 'compact'
        elif info['mode'] == InputType.ALBUM or info['mode'] == InputType.PLAYLIST or info['mode'] == InputType.ARTIST:
            webview_type = 'tall'

        print('data length:', len(info['data']))
        if info['response_type'] == ResponseType.SINGLE:
            for i in range(0, len(info['data']) if len(info['data']) <= 10 else 10):
                elements.append({
                    'title': info['data'][i]['title'],
                    'subtitle': info['data'][i]['subtitle'],
                    'image_url': info['data'][i]['widget_image_url'],
                    'default_action': {
                        'type': 'web_url',
                        'url': info['data'][i]['widget_song_url'],
                        'webview_height_ratio': webview_type
                    },
                    'buttons': self.produce_buttons(info, i)
                })
            return elements
        else:
            if info['top_element_style'] == 'large':
                elements = [{
                    'title': info['data'][0]['title'],
                    'image_url': info['data'][0]['widget_image_url'],
                    'default_action': {
                        'type': 'web_url',
                        'url': info['data'][0]['web_url'],
                        'webview_height_ratio': 'full'
                    }
                }]
                
                for i in range(1, len(info['data']) if len(info['data']) <= 4 else 4):
                    elements.append({
                        'title': info['data'][i]['title'],
                        'subtitle': info['data'][i]['subtitle'],
                        'image_url': info['data'][i]['widget_image_url'],
                        'default_action': {
                            'type': 'web_url',
                            'url': info['data'][i]['widget_song_url'],
                            'webview_height_ratio': 'compact'
                        }
                    })
                return elements
            else:
                #for i in range(0, info['num']):
                for i in range(0, len(info['data']) if len(info['data']) <= 4 else 4):
                    elements.append({
                        'title': info['data'][i]['title'],
                        'subtitle': info['data'][i]['subtitle'],
                        'image_url': info['data'][i]['widget_image_url'],
                        'default_action': {
                            'type': 'web_url',
                            'url': info['data'][i]['widget_song_url'] if info['mode'] != InputType.ARTIST else info['data'][i]['web_url'],
                            'webview_height_ratio': webview_type
                        }
                    })
                return elements


    def produce_buttons(self, info, index):
        buttons = []
        if info['response_type'] == ResponseType.SINGLE:
            buttons = [
            {
                'type': 'element_share'
            },
            {
                'type': 'web_url',
                'url': info['data'][index]['web_url'],
                'title': 'Web page'
            }]
            return buttons
        else:
            if info['top_element_style'] == 'large':
                buttons = [{
                    'type': 'web_url',
                    'url': info['data'][index]['web_url'],
                    'title': 'Web page'
                }]
                return buttons
            else:
                buttons = [{
                    'type': 'web_url',
                    'url': 'https://www.kkbox.com/tw/tc/search.php?word=' + info['token'],
                    'title': 'More'
                }]
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

    def set_start_button(self):
        data = {
            'get_started': {
                'payload': 'first_hand_shack'
            }
        }
        response = requests.post('https://graph.facebook.com/v2.6/me/messenger_profile?access_token=' + self.access_token, json=data)
        return response.content

    def set_sender_action(self, user_id, action):
        data = {
            'recipient': {
                'id': user_id
            },
            'sender_action': action
        }
        return self.send(data)

    def get_user_info(id):
        return requests.get('https://graph.facebook.com/v2.6/{USER_ID}?access_token={ACCESS_TOKEN}'.format(USER_ID=id, ACCESS_TOKEN=self.access_token))

def first_hand_shack(id, bot):
    bot.reply_text(id, ModeType.USER_MODE, '請輸入\"/歌曲名稱\"\n或輸入\"#專輯名稱\"\n或輸入\"$歌單名稱\"\n或輸入\"@歌手名稱\"')
    bot.set_sender_action(id, 'typing_off')
    try:
        dict = get_user_info(id)
        dict['user_id'] = id
        print(dict)
        #db.insert_new_row(dict)
    except:
        tb = sys.exc_info()
        print(tb[1])
        print(traceback.print_tb(tb[2]))
    return

def recieve_attachment(id):
    bot.reply_text(id, ModeType.USER_MODE, '❤️')
    bot.reply_text(id, ModeType.USER_MODE, '😁')
    bot.set_sender_action(id, 'typing_off')
    return 