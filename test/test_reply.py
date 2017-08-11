import unittest
import server


class GetReplyInfoTest(unittest.TestCase):
    def setUp(self):
        server.information.is_match = False

    def test_get_album_work(self):
        server.information._get_album('和自己對話')

    def test_get_artist_work(self):
        server.information._get_artist('Linkin Park')

    def test_get_playlist_work(self):
        server.information._get_playlist('西洋熱曲速播')

    def test_get_track_work(self):
        server.information._get_track('hello')

    def test_get_album_should_return_type_single(self):
        data = server.information._get_album('和自己對話')
        self.assertEqual(data['response_type'], server.util.ResponseType.SINGLE)

    def test_get_artist_should_return_type_single(self):
        data = server.information._get_artist('林俊傑')
        self.assertEqual(data['response_type'], server.util.ResponseType.LIST)

    def test_get_playlist_should_return_type_single(self):
        data = server.information._get_playlist('西洋新曲速報')
        self.assertEqual(data['response_type'], server.util.ResponseType.SINGLE)

    def test_get_track_should_return_type_single(self):
        data = server.information._get_track('生生')
        self.assertEqual(data['response_type'], server.util.ResponseType.SINGLE)

    def test_get_album_should_return_type_list(self):
        data = server.information._get_album('album_not_exist')
        self.assertEqual(data['response_type'], server.util.ResponseType.LIST)

    def test_get_artist_should_return_type_list(self):
        data = server.information._get_artist('park park')
        self.assertEqual(data['response_type'], server.util.ResponseType.LIST)

    def test_get_playlist_should_return_type_list(self):
        data = server.information._get_playlist('新曲速報')
        self.assertEqual(data['response_type'], server.util.ResponseType.LIST)

    def test_get_track_should_return_type_list(self):
        data = server.information._get_track('做夢')
        self.assertEqual(data['response_type'], server.util.ResponseType.LIST)

    def test_get_info_return_no_result(self):
        data = server.information.get_info('foobar_not_exist', server.util.InputType.PLAYLIST)
        self.assertEqual(data['mode'], server.util.ErrorType.NO_RESULT)


class ReplyTest(unittest.TestCase):
    def setUp(self):
        server.information.is_match = False

    def test_reply_single_will_work(self):
        info = server.information.get_info('Linkin Park', server.util.InputType.ARTIST)
        server.reply('1727613570586940', server.util.ModeType.USER_MODE, info)

    def test_reply_list_will_work(self):
        info = server.information.get_info('新曲速報', server.util.InputType.PLAYLIST)
        server.reply('1727613570586940', server.util.ModeType.USER_MODE, info)
