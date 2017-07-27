import unittest
import server


class UtilTest(unittest.TestCase):
    def test_get_summary_total(self):
        # Test error should return 0
        data = server.search('', 'album', 'TW')
        self.assertEqual(server.get_summary_total(data), 0)

        # Test total greater then 4 should return 4
        data = {'summary': {'total': '5'}}
        self.assertEqual(server.get_summary_total(data), 4)

        data = {'summary': {'total': '3'}}
        self.assertEqual(server.get_summary_total(data), 3)

    def test_parse_request(self):
        # test message is empty
        data = server.parse_request('')
        self.assertEqual(data['mode'], server.ErrorType.BAD_INPUT)
        
        # test message not start with special character (/#$@)
        data = server.parse_request('hello')
        self.assertEqual(data['mode'], server.ErrorType.BAD_INPUT)

        # test message start with /
        data = server.parse_request('/foobar')
        self.assertEqual(data['mode'], server.InputType.TRACK)
        self.assertEqual(data['token'], 'foobar')

        # test message start with #
        data = server.parse_request('#foobar')
        self.assertEqual(data['mode'], server.InputType.ALBUM)
        self.assertEqual(data['token'], 'foobar')

        # test message start with $
        data = server.parse_request('$foobar')
        self.assertEqual(data['mode'], server.InputType.PLAYLIST)
        self.assertEqual(data['token'], 'foobar')

        # test message start with @
        data = server.parse_request('@foobar')
        self.assertEqual(data['mode'], server.InputType.ARTIST)
        self.assertEqual(data['token'], 'foobar')