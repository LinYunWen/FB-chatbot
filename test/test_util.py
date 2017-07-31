import unittest
import server
from server.util import *


class UtilTest(unittest.TestCase):
    def test_get_summary_total(self):
        # Test error should return 0
        data = server.search('', 'album', 'TW')
        self.assertEqual(get_summary_total(data), 0)

        # Test total greater then 4 should return 4
        data = {'summary': {'total': '5'}}
        self.assertEqual(get_summary_total(data), 4)

        data = {'summary': {'total': '3'}}
        self.assertEqual(get_summary_total(data), 3)

    def test_parse_request(self):
        # test message is empty
        data = parse_request('')
        self.assertEqual(data['mode'], ErrorType.BAD_INPUT)
        
        # test message not start with special character (/#$@)
        data = parse_request('hello')
        self.assertEqual(data['mode'], ErrorType.BAD_INPUT)

        # test message start with /
        data = parse_request('/foobar')
        self.assertEqual(data['mode'], InputType.TRACK)
        self.assertEqual(data['token'], 'foobar')

        # test message start with #
        data = parse_request('#foobar')
        self.assertEqual(data['mode'], InputType.ALBUM)
        self.assertEqual(data['token'], 'foobar')

        # test message start with $
        data = parse_request('$foobar')
        self.assertEqual(data['mode'], InputType.PLAYLIST)
        self.assertEqual(data['token'], 'foobar')

        # test message start with @
        data = parse_request('@foobar')
        self.assertEqual(data['mode'], InputType.ARTIST)
        self.assertEqual(data['token'], 'foobar')