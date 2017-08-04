# -*- coding: utf-8 -*-

import requests
from server.util import ErrorType, InputType, ResponseType, ModeType


class Fbmsg(object):
    def __init__(self, access_token):
        self.access_token = access_token

    def send(self, data):
        response = requests.post('https://graph.facebook.com/v2.6/me/messages?access_token=' + self.access_token, json=data)
        print(response.content)
        return response.content

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
        return self.send(data) if mode == ModeType.USER_MODE else self.broadcast_send(data, filter={})

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
        return self.send(data) if mode == ModeType.USER_MODE else self.broadcast_send(data, filter={})

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
        return self.send(data) if mode == ModeType.USER_MODE else self.broadcast_send(data, filter={})

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
        return self.send(data) if mode == ModeType.USER_MODE else self.broadcast_send(data, filter={})

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

    def broadcast_send(data, filter):
        cur.execute('SELECT user_id from audience')
        rows = cur.fetchall()
        for row in rows:
            print('row', row)
            data['recipient']['id'] = row
            self.send(data)
        return  self.reply_text('1727613570586940', 'finished broadcast sending')
