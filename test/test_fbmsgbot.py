import unittest
import server


class FbMsgBotTest(unittest.TestCase):
    def setUp(self):
        server.ACCESS_TOKEN = 'EAAEtsX9w5Q0BAHz42VnrkeSNajWpvJjc8ONCs4plPKlBzoafvDTxTEkVY1gGmTxiDcPKauUVHmACxSoyJ715dwhuvRV78QZCWKrQNnACFevghRzjU33xWYFuwZChpDTsVpnSZCtKmZBayMzOzXFdiWly9OZAJPgjgptYzBZAnivwZDZD'

    def test_reply_text_work(self):
        data = server.reply_text('10', 'hello')

    def test_greeting_message_work(self):
        data = server.reply_greeting_message()

    def test_reply_image_url_work(sef):
        data = server.reply_image_url('10', 'https://i.imgur.com/OK7XeWs.png')

    def test_reply_generic_template_work(self):
        info = server._get_track('生生')
        data = server.reply_generic_template('10', info)
    
    def test_reply_list_template_work(self):
        info = server._get_track('no exactly match')
        data = server.reply_list_template('10', info)

    def test_reply_text_correct(self):
        data = server.reply_text('10', 'hello')
        self.assertEqual(data['text'], 'hello')

    