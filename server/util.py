# -*- coding: utf-8 -*-

import enum
import requests

class InputType(enum.Enum):
    TRACK = 'track'
    ALBUM = 'album'
    PLAYLIST = 'playlist'
    ARTIST = 'artist'
    INQUERY = 'inquery'


class ResponseType(enum.Enum):
    SINGLE = 'single'
    LIST = 'list'


class ErrorType(enum.Enum):
    BAD_INPUT = 'bad_input'
    NO_RESULT = 'no_result'
    SOMETHING_WRONG = 'something_wrong'


def get_summary_total(json):
    # Check if the json has error
    if 'error' in json:
        return 0

    total = int(json["summary"]["total"])
    return 4 if total > 4 else total

def get_widget_url(id, input_type):
    return "https://widget.kkbox.com/v1/?id=" + id + "&type=" + input_type

def parse_request(message):
    result = {'mode': ErrorType.BAD_INPUT, 'token': ''}

    if not message or len(message) < 2:
        return result

    input_type = message[0]
    result['token'] = message[1:]
    
    if input_type == '/' or input_type == '／':
        result["mode"] = InputType.TRACK
    elif input_type == '#' or input_type == '＃':
        result["mode"] = InputType.ALBUM
    elif input_type == '$' or input_type == '＄':
        result["mode"] = InputType.PLAYLIST
    elif input_type == '@' or input_type == '＠':
        result["mode"] = InputType.ARTIST
    
    return result

def modify_image_size(url, size):
    index = url.rfind("/")
    # print(index)
    if index > 0:
        temp = url[index + 1:]
        want_size = str(size) + "x" + str(size) + ".jpg"
        # print(size)
        if temp != want_size:
            # print(url[0:index+1] + "300x300.jpg")
            return url[0:index + 1] + want_size
        else:
            return url
    else:
        return url

def artist_songs(id, territory):
    headers = {"Authorization": "Bearer FDP48nJQc7DJD9MJtkhVqA=="}
    return requests.get("https://api.kkbox.com/v1.1/artists/" + id + "/top-tracks?territory=" + territory + "&limit=3",
                        headers=headers).json()

def search(inquiry, type, territory):
    payload = {"q": inquiry, "type": type, "territory": territory}
    headers = {"Authorization": "Bearer FDP48nJQc7DJD9MJtkhVqA=="}

    response = requests.get("https://api.kkbox.com/v1.1/search", params=payload, headers=headers)
    return response.json()