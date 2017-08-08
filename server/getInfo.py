# -*- coding: utf-8 -*-

import sys, traceback
from server import util
from server.util import ErrorType, InputType, ResponseType, ModeType
from server import fbmsg

is_match = False

def matching_result(input, expect):
    global is_match
    is_match = False

    index = expect.find('(')
    if index >= 0:
        if index >= 2:
            expect_pre = expect[:index-1]
            is_match = True if input.lower() == expect_pre.lower() else False
    else:
        is_match = True if input.lower() == expect.lower() else False
    return is_match

def get_info(msg, info_type):
    global is_match
    get = {
        InputType.TRACK: _get_track,
        InputType.ALBUM: _get_album,
        InputType.PLAYLIST: _get_playlist,
        InputType.ARTIST: _get_artist,
    }
    is_match = False

    try:
        info = get[info_type](msg)
    except:
        tb = sys.exc_info()
        print(tb[1])
        print(traceback.print_tb(tb[2]))
        return {'mode':ErrorType.SOMETHING_WRONG}
    return info

def _get_reply(msg, type, id):
    if type.value == 'track' and id != 'none':
        search_result = util.artist_songs(id, 'TW')
    else:
        search_result = util.search(msg, type.value, 'TW')
    total = util.get_summary_total(search_result)

    if not total:
        return {'mode': ErrorType.NO_RESULT}

    data = []
    match = None
    for d in search_result[type.value + 's']['data'] if id == 'none' else search_result['data']:
        # set title and subtitle
        title = d['name'] if 'name' in d else d['title']
        subtitle = util.set_subtitle(type, d)
        
        pk = d['id']
        widget_url = util.get_widget_url(pk, type.value if type.value != 'track' else 'song')

        data.append({
            'title': title,
            'subtitle': subtitle,
            'widget_song_url': widget_url,
            'widget_image_url': d['images'][-1]['url'] if 'images' in d else d['album']['images'][-1]['url'],
            'web_url': d['url']
        })

        # XXX: WTF? what does this if stmt do?
        if id == 'none' and not is_match and matching_result(msg, title):
            match = data[-1]
            if type.value == 'artist':
                return {'id':pk, 'data':match}

    # Replace 1st item to match data
    if id == 'none' and is_match and match:
        data.remove(match)
        data.insert(0, match)

    return {
        'mode': type,
        'response_type': ResponseType.SINGLE if is_match or len(data) < 2 else ResponseType.LIST,
        'top_element_style': 'compact' if id == 'none' else 'large',
        'data': data,
        'token': msg,
    }

def _get_album(msg):
    return _get_reply(msg, InputType.ALBUM, 'none')

def _get_playlist(msg):
    return _get_reply(msg, InputType.PLAYLIST, 'none')

def _get_artist(msg):
    global is_match
    data = _get_reply(msg, InputType.ARTIST, 'none')
    if is_match:
        id = data['id']
        artist_data = data['data']
        is_match = False
        track_data = _get_reply(msg, InputType.TRACK, id)
        track_data['data'].insert(0, artist_data)
        data = track_data
    return data

def _get_track(msg):
    return _get_reply(msg, InputType.TRACK, 'none')