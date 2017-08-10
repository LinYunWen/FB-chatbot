import os
import unittest
import server.connectDB
import server


class FbMsgUtilTest(unittest.TestCase):
    def setUp(self):
        server.getInfo.is_match = False

    def test_produce_buttons_single(self):
        expect = [{
            'type': 'element_share'
        }, {
            'type': 'web_url',
            'url': 'https://event.kkbox.com/content/song/DZvlIxxKM7Esr3l8Gi',
            'title': 'Web page'
        }]
        info = server.getInfo._get_track('生生')
        self.assertEqual(server.client.produce_buttons(info, 0), expect)

    def test_produce_buttons_list(self):
        expect = [{
            'type': 'web_url',
            'url': 'https://www.kkbox.com/tw/tc/search.php?word=button_not_list',
            'title': 'More'
        }]
        info = server.getInfo._get_track('button_not_list')
        # print(server.client.produce_buttons(info))
        self.assertEqual(server.client.produce_buttons(info, 0), expect)

    def test_produce_elements_single(self):
        expect = [{
            'title': '生生 (The Beacon)', 'subtitle': '林俊傑 (JJ Lin)\n新地球 (Genesis)', 'image_url': 'https://i.kfs.io/album/tw/5197882,2v2/fit/1000x1000.jpg', 'default_action': {'type': 'web_url', 'url': 'https://widget.kkbox.com/v1/?id=DZvlIxxKM7Esr3l8Gi&type=song', 'webview_height_ratio': 'compact'}, 'buttons': [{'type': 'element_share'}, {'type': 'web_url', 'url': 'https://event.kkbox.com/content/song/DZvlIxxKM7Esr3l8Gi', 'title': 'Web page'}]}, {
            'title': '生生 (The Beacon)', 'subtitle': '林俊傑 (JJ Lin)\n新地球 - 人', 'image_url': 'https://i.kfs.io/album/tw/5670674,0v1/fit/1000x1000.jpg', 'default_action': {'type': 'web_url', 'url': 'https://widget.kkbox.com/v1/?id=OkMturW3wySdJYrtlx&type=song', 'webview_height_ratio': 'compact'}, 'buttons': [{'type': 'element_share'}, {'type': 'web_url', 'url': 'https://event.kkbox.com/content/song/OkMturW3wySdJYrtlx', 'title': 'Web page'}]}, {
            'title': '生生世世', 'subtitle': '陳淑樺 (Sarah Chen)\n生生世世', 'image_url': 'https://i.kfs.io/album/tw/35387,0v1/fit/1000x1000.jpg', 'default_action': {'type': 'web_url', 'url': 'https://widget.kkbox.com/v1/?id=5X-SWVA_ELRufxUAxt&type=song', 'webview_height_ratio': 'compact'}, 'buttons': [{'type': 'element_share'}, {'type': 'web_url', 'url': 'https://event.kkbox.com/content/song/5X-SWVA_ELRufxUAxt', 'title': 'Web page'}]}, {
            'title': '生生世世愛', 'subtitle': 'Various Artists\n仙劍奇俠傳三 電視原聲帶', 'image_url': 'https://i.kfs.io/album/tw/139215,0v1/fit/1000x1000.jpg', 'default_action': {'type': 'web_url', 'url': 'https://widget.kkbox.com/v1/?id=8tKrqGfjsnPsExOKai&type=song', 'webview_height_ratio': 'compact'}, 'buttons': [{'type': 'element_share'}, {'type': 'web_url', 'url': 'https://event.kkbox.com/content/song/8tKrqGfjsnPsExOKai', 'title': 'Web page'}]}, {
            'title': '生生世世', 'subtitle': '陳淑樺 (Sarah Chen)\n給淑樺的一封信', 'image_url': 'https://i.kfs.io/album/tw/79501,0v3/fit/1000x1000.jpg', 'default_action': {'type': 'web_url', 'url': 'https://widget.kkbox.com/v1/?id=8maS6lLQJRsanvCbEd&type=song', 'webview_height_ratio': 'compact'}, 'buttons': [{'type': 'element_share'}, {'type': 'web_url', 'url': 'https://event.kkbox.com/content/song/8maS6lLQJRsanvCbEd', 'title': 'Web page'}]}, {
            'title': '生生世世', 'subtitle': '陳淑樺 (Sarah Chen)\n情牽淑樺', 'image_url': 'https://i.kfs.io/album/tw/38094,0v3/fit/1000x1000.jpg', 'default_action': {'type': 'web_url', 'url': 'https://widget.kkbox.com/v1/?id=5YDD0u13hYuu1M4h_8&type=song', 'webview_height_ratio': 'compact'}, 'buttons': [{'type': 'element_share'}, {'type': 'web_url', 'url': 'https://event.kkbox.com/content/song/5YDD0u13hYuu1M4h_8', 'title': 'Web page'}]}, {
            'title': '生生不息', 'subtitle': '心靈音樂館\n心靈音樂館 (3CD)', 'image_url': 'https://i.kfs.io/album/tw/311728,0v1/fit/1000x1000.jpg', 'default_action': {'type': 'web_url', 'url': 'https://widget.kkbox.com/v1/?id=Cos5F_f9HOVZivtEbb&type=song', 'webview_height_ratio': 'compact'}, 'buttons': [{'type': 'element_share'}, {'type': 'web_url', 'url': 'https://event.kkbox.com/content/song/Cos5F_f9HOVZivtEbb', 'title': 'Web page'}]}, {
            'title': '生生世世', 'subtitle': '陳淑樺 (Sarah Chen)\n滾石香港黃金十年-陳淑樺精選', 'image_url': 'https://i.kfs.io/album/global/9487150,0v1/fit/1000x1000.jpg', 'default_action': {'type': 'web_url', 'url': 'https://widget.kkbox.com/v1/?id=8sCmOc6dV0ZqnZoaAW&type=song', 'webview_height_ratio': 'compact'}, 'buttons': [{'type': 'element_share'}, {'type': 'web_url', 'url': 'https://event.kkbox.com/content/song/8sCmOc6dV0ZqnZoaAW', 'title': 'Web page'}]}, {
            'title': '生生不息(Pulsating Life)', 'subtitle': 'ASIAN KUNG-FU GENERATION\n到未知的明天(Into an Unseen Tomorrow)', 'image_url': 'https://i.kfs.io/album/tw/106389,0v1/fit/1000x1000.jpg', 'default_action': {'type': 'web_url', 'url': 'https://widget.kkbox.com/v1/?id=Gk_p8m7-nSw3Swd93H&type=song', 'webview_height_ratio': 'compact'}, 'buttons': [{'type': 'element_share'}, {'type': 'web_url', 'url': 'https://event.kkbox.com/content/song/Gk_p8m7-nSw3Swd93H', 'title': 'Web page'}]}, {
            'title': '生生不息', 'subtitle': '心靈甦醒\n心靈甦醒-古箏音樂系列 (3CD)', 'image_url': 'https://i.kfs.io/album/tw/311739,0v1/fit/1000x1000.jpg', 'default_action': {'type': 'web_url', 'url': 'https://widget.kkbox.com/v1/?id=Kr5TvxRH6Il0DOF65g&type=song', 'webview_height_ratio': 'compact'}, 'buttons': [{'type': 'element_share'}, {'type': 'web_url', 'url': 'https://event.kkbox.com/content/song/Kr5TvxRH6Il0DOF65g', 'title': 'Web page'}]}]
        info = server.getInfo._get_track('生生')
        self.assertEqual(server.client.produce_elements(info), expect)

    def test_produce_elements_list(self):
        expect = [{
            'title': 'The Newspaper Is Not Listed', 'subtitle': 'Various Artists\nSoundz Like Fun, Vol. 3', 'image_url': 'https://i.kfs.io/album/global/26592087,0v1/fit/1000x1000.jpg', 'default_action': {'type': 'web_url', 'url': 'https://widget.kkbox.com/v1/?id=_XgIO-De0EWg8pB_Ia&type=song', 'webview_height_ratio': 'compact'}}, {
            'title': "Ain't nothing gonna break it", 'subtitle': "Listed-not\nAin't nothing gonna break it (Ain't nothing gonna break it)", 'image_url': 'https://i.kfs.io/album/global/19779662,0v1/fit/1000x1000.jpg', 'default_action': {'type': 'web_url', 'url': 'https://widget.kkbox.com/v1/?id=HZ4KZgKiEYKfnyn02i&type=song', 'webview_height_ratio': 'compact'}}, {
            'title': 'Inside Of You', 'subtitle': 'Listed-not\nPROMISED PLACE (PROMISED PLACE)', 'image_url': 'https://i.kfs.io/album/global/4196016,0v1/fit/1000x1000.jpg', 'default_action': {'type': 'web_url', 'url': 'https://widget.kkbox.com/v1/?id=GnFLK6nmJNIVIUfPMr&type=song', 'webview_height_ratio': 'compact'}}, {
            'title': 'Until It Arrives', 'subtitle': 'Listed-not\nPROMISED PLACE (PROMISED PLACE)', 'image_url': 'https://i.kfs.io/album/global/4196016,0v1/fit/1000x1000.jpg', 'default_action': {'type': 'web_url', 'url': 'https://widget.kkbox.com/v1/?id=0pFTD8JFMinpWQtf64&type=song', 'webview_height_ratio': 'compact'}}]
        info = server.getInfo._get_track('button_not_list')
        self.assertEqual(server.client.produce_elements(info), expect)

    def test_get_user_info(self):
        expect = {
            'first_name': 'Yun-wen',
            'last_name': 'Lin',
            'profile_pic': 'https://scontent.xx.fbcdn.net/v/t1.0-1/13407264_793420647424214_3630625782716408607_n.jpg?oh=69ba27a01d2c378292fe5646ea32eda1&oe=59F511A4',
            'locale': 'zh_TW',
            'timezone': 8,
            'gender': 'male'
        }
        data = server.client.get_user_info('1727613570586940')
        self.assertEqual(data, expect)


class FbMsgBotTest(unittest.TestCase):
    def setUp(self):
        self.user_id = '1727613570586940'
        server.getInfo.is_match = False

    def test_reply_text_work(self):
        data = server.client.reply_text(
            self.user_id, server.util.ModeType.USER_MODE, 'hello')

    def test_greeting_message_work(self):
        data = server.client.reply_greeting_message()

    def test_reply_image_url_work(self):
        data = server.client.reply_image_url(
            self.user_id, server.util.ModeType.USER_MODE, 'https://i.imgur.com/OK7XeWs.png')

    def test_reply_generic_template_work(self):
        info = server.getInfo._get_track('生生')
        data = server.client.reply_generic_template(
            self.user_id, server.util.ModeType.USER_MODE, info)

    def test_reply_list_template_large_work(self):
        info = server.getInfo._get_artist('林俊傑')
        data = server.client.reply_list_template(
            self.user_id, server.util.ModeType.USER_MODE, info)

    def test_reply_list_template_compact_work(self):
        info = server.getInfo._get_playlist('下雨')
        data = server.client.reply_list_template(
            self.user_id, server.util.ModeType.USER_MODE, info)

    def test_first_hand_shack_work(self):
        server.fbmsg.first_hand_shack(self.user_id, server.client)

    def test_recieve_attachment(self):
        server.fbmsg.recieve_attachment(self.user_id, server.client)


class DatabseConnectionTest(unittest.TestCase):
    def connection_work(self):
        connectDB.connect_database()
