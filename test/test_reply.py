import unittest
import server


class ReplyTest(unittest.TestCase):
    def test_get_album(self):
        server._get_album('和自己對話')

    def test_get_artist(self):
        server._get_artist('Linkin Park')

    def test_get_playlist(self):
        server._get_playlist('西洋熱曲速播')

    def test_get_track(self):
        server._get_track('hello')
