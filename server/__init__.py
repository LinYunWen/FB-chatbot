# -*- coding: utf-8 -*-

import os
import requests
from flask import Flask, request
from pymessenger.bot import Bot

from server import util
from server.util import ErrorType, InputType, ResponseType
from server.fbmsg import Fbmsg


app = Flask(__name__)

# this is a token to match FB fans page
# Light up
# ACCESS_TOKEN = "EAAEtsX9w5Q0BAHz42VnrkeSNajWpvJjc8ONCs4plPKlBzoafvDTxTEkVY1gGmTxiDcPKauUVHmACxSoyJ715dwhuvRV78QZCWKrQNnACFevghRzjU33xWYFuwZChpDTsVpnSZCtKmZBayMzOzXFdiWly9OZAJPgjgptYzBZAnivwZDZD"
# test bot
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
bot = Bot(ACCESS_TOKEN)
client = Fbmsg(ACCESS_TOKEN)

is_match = False


# for verify
@app.route("/", methods=["GET"])
def handle_verification():
    if request.args["hub.verify_token"] == "test_for_verify":
        return request.args["hub.challenge"]
    else:
        return "Wrong Verify Token"

def get_access_token():
    return 0

def handle_error_request(user_id, error_type):
    if error_type == ErrorType.BAD_INPUT:
        client.reply_text(user_id, "未設定之指令")
        client.reply_text(user_id, "請輸入\"/歌曲名稱\"\n或輸入\"#專輯名稱\"\n或輸入\"$歌單名稱\"\n或輸入\"@歌手名稱\"")
    elif error_type == ErrorType.NO_RESULT:
        client.reply_text(user_id, "抱歉～沒有尋找到任何資料")

    return 0


def search(inquiry, type, territory):
    payload = {"q": inquiry, "type": type, "territory": territory}
    headers = {"Authorization": "Bearer FDP48nJQc7DJD9MJtkhVqA=="}

    response = requests.get("https://api.kkbox.com/v1.1/search", params=payload, headers=headers)
    # print("content: ",response.json())
    # print("url: ",response.url)
    return response.json()

def matching_result(input, expect):
    global is_match
    is_match = expect.startswith(input)   
    return expect.startswith(input)


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
    except KeyError:
        return ''
    return info

def _get_reply(msg, type):
    search_result = search(msg, type.value, 'TW')
    total = util.get_summary_total(search_result)

    if not total:
        return {'mode': ErrorType.NO_RESULT}

    data = []
    match = None
    for d in search_result[type.value + 's']['data']:
        title = d['name'] if 'name' in d else d['title']

        pk = d['id']
        widget_url = util.get_widget_url(pk, type.value if type.value != InputType.TRACK else 'song')

        data.append({
            'title': title,
            'subtitle': d['artist']['name'] if 'artist' in d else title,
            'widget_song_url': widget_url,
            'widget_image_url': d['images'][-1]['url'] if 'images' in d else d['album']['images'][-1]['url'],
            'web_url': d['url']
        })

        # XXX: WTF? what does this if stmt do?
        if not is_match and matching_result(msg, title):
           match = data[-1]

    # Replace 1st item to match data
    if is_match and match:
        data.insert(0, match)

    return {
        'mode': type,
        'response_type': ResponseType.SINGLE if is_match else ResponseType.LIST,
        'top_element_style': 'compact',
        'data': data,
        'token': msg,
    }


    

def _get_album(msg):
    return _get_reply(msg, InputType.ALBUM)
    

def _get_playlist(msg):
    return _get_reply(msg, InputType.PLAYLIST)


def _get_artist(msg):
    return _get_reply(msg, InputType.ARTIST)


def _get_track(msg):
    return _get_reply(msg, InputType.TRACK)

    # tracks = search(msg, 'track', 'TW')
    # num = get_summary_total(tracks)

    # # If result is empty, fast fail
    # if not num:
    #     return {'mode': ErrorType.NO_RESULT}

    # # Check if we match the track
    # for track in tracks['tracks']['data']:
    #     #if msg.lower() in track['name'].lower():
    #     if matching_result(msg, track["name"]):
    #         track_id = track['id']
    #         track_widget_url = get_widget_url(track_id, "song")

    #         return {
    #             'mode': InputType.TRACK,
    #             'response_type': ResponseType.SINGLE,
    #             'title': track['name'],
    #             'subtitle': '{album} {artist}'.format(album=track['album']['name'], artist=track['album']['artist']['name']),
    #             'widget_song_url': track_widget_url,
    #             'widget_image_url': track['album']['images'][-1]['url'],
    #             'web_url': track['url']
    #         }


    # # Return items when length > 0
    # if tracks['tracks']['data']:
    #     pass

    # return {'mode': ErrorType.NO_RESULT}


def reply(user_id, info):
    client.set_sender_action(user_id, "mark_seen")
    client.set_sender_action(user_id, "typing_on")

    if info["response_type"] == ResponseType.SINGLE:
        client.reply_generic_template(user_id, info)
    elif info["response_type"] == ResponseType.LIST:
        if info["top_element_style"] == "compact":
            if info["mode"] == InputType.TRACK or info["mode"] == InputType.ARTIST:
                client.reply_text(user_id, "抱歉~沒有找到完全相同者\n請問是以下選項嗎？")
        client.reply_list_template(user_id, info)
    return 'ok'


@app.route("/", methods=["POST"])
def handle_incoming_message():
    data = request.json
    messaging = data["entry"][0]["messaging"][0]
    sender_id = messaging["sender"]["id"]

    # handle first conversation
    if "postback" in messaging:
        if messaging["postback"]["payload"] == "first_hand_shack":
            client.reply_text(sender_id, "請輸入\"/歌曲名稱\"\n或輸入\"#專輯名稱\"\n或輸入\"$歌單名稱\"\n或輸入\"@歌手名稱\"")
            return "ok"

    # request with not pure text message
    if "attachments" in messaging["message"]:
        response = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=data)
        return "ok"

    # Pure text message
    text = messaging["message"]["text"]
    print("message: ", text)
    request_token = parse_request(text)
    if request_token["mode"] in ErrorType:
        handle_error_request(sender_id, request_token["mode"])
    else:
        info = get_info(request_token["token"], request_token["mode"])
        reply(sender_id, info)

    return "ok"


if __name__ == "__main__":
    client.set_start_button()
    app.run(debug=True)