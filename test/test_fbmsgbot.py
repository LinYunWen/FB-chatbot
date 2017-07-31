import os
import unittest
import server


class FbMsgUtilTest(unittest.TestCase):
    def test_produce_buttons_single(self):
        expect = [{
            'type': 'web_url',
            'url': 'https://event.kkbox.com/content/song/DZvlIxxKM7Esr3l8Gi',
            'title': 'Web page'
        }]
        info = server._get_track('生生')
        self.assertEqual(server.client.produce_buttons(info), expect)

    def test_produce_buttons_list(self):
        expect = [{
            'type': 'web_url',
            'url': 'https://www.kkbox.com/tw/tc/search.php?word=button_not_list',
            'title': 'More'
        }]
        info = server._get_track('button_not_list')
        print(server.client.produce_buttons(info))
        self.assertEqual(server.client.produce_buttons(info), expect)

    def test_produce_elements_single(self):
        expect = [{
            'title': '生生 (The Beacon)',
            'subtitle': '生生 (The Beacon)',
            'image_url': 'https://i.kfs.io/album/tw/5197882,2v2/fit/1000x1000.jpg',
            'default_action': {
                'type': 'web_url',
                'url': 'https://widget.kkbox.com/v1/?id=DZvlIxxKM7Esr3l8Gi&type=track',
                'webview_height_ratio': 'compact'
            },
            'buttons': [
                {
                    'type': 'web_url',
                    'url': 'https://event.kkbox.com/content/song/DZvlIxxKM7Esr3l8Gi',
                    'title': 'Web page'
                }
            ]
        }]
        info = server._get_track('生生')
        self.assertEqual(server.client.produce_elements(info), expect)

    def test_produce_elements_list(self):
        expect = [
            {
                'title': 'The Newspaper Is Not Listed',
                'subtitle': 'The Newspaper Is Not Listed',
                'image_url': 'https://i.kfs.io/album/global/26592087,0v1/fit/1000x1000.jpg',
                'default_action': {
                    'type': 'web_url',
                    'url': 'https://widget.kkbox.com/v1/?id=_XgIO-De0EWg8pB_Ia&type=track',
                    'webview_height_ratio': 'compact'
                }
            }, {
                'title': "Ain't nothing gonna break it",
                'subtitle': "Ain't nothing gonna break it",
                'image_url': 'https://i.kfs.io/album/global/19779662,0v1/fit/1000x1000.jpg',
                'default_action': {
                    'type': 'web_url',
                    'url': 'https://widget.kkbox.com/v1/?id=HZ4KZgKiEYKfnyn02i&type=track',
                    'webview_height_ratio': 'compact'
                }
            }, {
                'title': 'Inside Of You',
                'subtitle': 'Inside Of You',
                'image_url': 'https://i.kfs.io/album/global/4196016,0v1/fit/1000x1000.jpg',
                'default_action': {
                    'type': 'web_url',
                    'url': 'https://widget.kkbox.com/v1/?id=GnFLK6nmJNIVIUfPMr&type=track',
                    'webview_height_ratio': 'compact'
                }
            }, {
                'title': 'Until It Arrives',
                'subtitle': 'Until It Arrives',
                'image_url': 'https://i.kfs.io/album/global/4196016,0v1/fit/1000x1000.jpg',
                'default_action': {
                    'type': 'web_url',
                    'url': 'https://widget.kkbox.com/v1/?id=0pFTD8JFMinpWQtf64&type=track',
                    'webview_height_ratio': 'compact'
                }
            }
        ]
        info = server._get_track('button_not_list')
        self.assertEqual(server.client.produce_elements(info), expect)


class FbMsgBotTest(unittest.TestCase):
    def setUp(self):
        self.user_id = '10'
        #server.ACCESS_TOKEN = 'EAAEtsX9w5Q0BAHz42VnrkeSNajWpvJjc8ONCs4plPKlBzoafvDTxTEkVY1gGmTxiDcPKauUVHmACxSoyJ715dwhuvRV78QZCWKrQNnACFevghRzjU33xWYFuwZChpDTsVpnSZCtKmZBayMzOzXFdiWly9OZAJPgjgptYzBZAnivwZDZD'


    def test_reply_text_work(self):
        data = server.client.reply_text(self.user_id, 'hello')

    def test_greeting_message_work(self):
        data = server.client.reply_greeting_message()

    def test_reply_image_url_work(self):
        data = server.client.reply_image_url(self.user_id, 'https://i.imgur.com/OK7XeWs.png')

    def test_reply_generic_template_work(self):
        info = server._get_track('生生')
        data = server.client.reply_generic_template(self.user_id, info)
    
    def test_reply_list_template_work(self):
        info = server._get_track('no exactly match')
        data = server.client.reply_list_template(self.user_id, info)


    