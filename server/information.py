# -*- coding: utf-8 -*-

import sys, traceback
from server import util
from server.util import ErrorType, InputType, ResponseType, ModeType
import fbmsg

# global variable for if match search result
is_match = False

def matching_result(input, expect):
    # to match retrieved data and user input
    # @input: the key word which user inputed
    # @expect: the title got result after searching
    global is_match
    is_match = False

    # discard words after '(' and character ' '
    index = expect.find('(')
    space_index = index
    if index >= 0:
        if index >= 2:
            expect_pre = expect[:index-1]
            while True and len(expect_pre) >= 2:
                space_index = expect_pre.rfind(' ', 0, space_index-1)
                if space_index < 0:
                    break
                expect_pre = expect_pre[:space_index]
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
    # process data before reply
    # @msg: the key word which user input
    # @type; InputType
    # @id: artist id (it will be 'none' if type != InputType.Track after searching artist)

    while True:
        if type.value == 'track' and id != 'none':
            search_result = util.artist_songs(id, 'TW')
        else:
            search_result = util.search(msg, type.value, 'TW')
        
        if 'error' in search_result:
            if search_result['error']['message'] == "Invalid Authorication":
                util.update_authorization(util.get_access_token())
                continue
        break
    
    if type.value == 'track' and id != 'none':
        search_result = util.artist_songs(id, 'TW')
    else:
        search_result = util.search(msg, type.value, 'TW')

    total = util.get_summary_total(search_result)

    # check retrieved data is not empty
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

        # get match
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

def _get_track(msg):
    return _get_reply(msg, InputType.TRACK, 'none')

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