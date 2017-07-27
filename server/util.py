# -*- coding: utf-8 -*-

import enum

class InputType(enum.Enum):
    TRACK = 'track'
    ALBUM = 'album'
    PLAYLIST = 'playlist'
    ARTIST = 'artist'
    INQUERY = 'inquery'


class ResponseType(enum.Enum):
    SINGLE = 0
    LIST = 1


class ErrorType(enum.Enum):
    BAD_INPUT = -1
    NO_RESULT = -2


def get_summary_total(json):
    # Check if the json has error
    if 'error' in json:
        return 0

    total = int(json["summary"]["total"])
    return 4 if total > 4 else total


def parse_request(message):
    result = {'mode': ErrorType.BAD_INPUT, 'token': ''}

    if not message or len(message) < 2:
        return result

    input_type = message[0]
    result['token'] = message[1:]
    
    if input_type == '/':
        result["mode"] = InputType.TRACK
    elif input_type == '#':
        result["mode"] = InputType.ALBUM
    elif input_type == '$':
        result["mode"] = InputType.PLAYLIST
    elif input_type == '@':
        result["mode"] = InputType.ARTIST
    
    return result


