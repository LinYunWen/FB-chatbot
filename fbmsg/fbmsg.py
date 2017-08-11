# -*- coding: utf-8 -*-

import fbmsg.sender
from server.util import ErrorType, InputType, ResponseType, ModeType

class Bot(object):
    def __init__(self, access_token):
        self.access_token = access_token

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
        # print(elements)
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
        return fbmsg.sender.send(self.access_token, data) if mode == ModeType.USER_MODE else self.broadcast_send(self.access_token, data)

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
        return fbmsg.sender.send(self.access_token, data) if mode == ModeType.USER_MODE else self.broadcast_send(self.access_token, data)

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
        return fbmsg.sender.send(self.access_token, data) if mode == ModeType.USER_MODE else self.broadcast_send(self.access_token, data)

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
        return fbmsg.sender.send(self.access_token, data) if mode == ModeType.USER_MODE else self.broadcast_send(self.access_token, data)

    def set_sender_action(self, user_id, action):
        data = {
            'recipient': {
                'id': user_id
            },
            'sender_action': action
        }
        return fbmsg.sender.send(self.access_token, data)
