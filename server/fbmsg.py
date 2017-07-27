# -*- coding: utf-8 -*-
import requests
from server.util import *


def produce_elements(info):
    elements = []
    if info["mode"] == InputType.TRACK:
        webview_type = "compact"
    elif info["mode"] == InputType.ALBUM or info["mode"] == InputType.PLAYLIST or info["mode"] == InputType.ARTIST:
        webview_type = "tall"

    if info["response_type"] == ResponseType.SINGLE:
        elements.append({
            "title": info['data'][0]["title"],
            "subtitle": info['data'][0]["subtitle"],
            "image_url": info['data'][0]["widget_image_url"],
            "default_action": {
                "type": "web_url",
                "url": info['data'][0]["widget_song_url"],
                "webview_height_ratio": webview_type
            },
            "buttons": produce_buttons(info)
        })
        # print(elements)
        return elements
    else:
        if info["top_element_style"] == "large":
            elements = [{
                "title": info["data"][0]["title"],
                "image_url": info["data"][0]["image_url"],
                "default_action": {
                    "type": "web_url",
                    "url": info["data"][0]["url"],
                    "webview_height_ratio": "full"
                }
            }]
            for i in range(1, info["num"] + 1):
                elements.append({
                    "title": info["data"][i]["title"],
                    "subtitle": info["data"][i]["subtitle"],
                    "image_url": info["data"][i]["widget_image_url"],
                    "default_action": {
                        "type": "web_url",
                        "url": info["data"][i]["widget_song_url"],
                        "webview_height_ratio": "compact"
                    }
                })
            return elements

        else:
            #for i in range(0, info["num"]):
            for i in range(0,4):
                elements.append({
                    "title": info["data"][i]["title"],
                    "subtitle": info["data"][i]["subtitle"],
                    "image_url": info["data"][i]["widget_image_url"],
                    "default_action": {
                        "type": "web_url",
                        "url": info["data"][i]["widget_song_url"],
                        "webview_height_ratio": webview_type
                    }
                })
            return elements


def produce_buttons(info):
    buttons = []
    if info["response_type"] == ResponseType.SINGLE:
        buttons = [{
            "type": "web_url",
            "url": info['data'][0]["web_url"],
            "title": "Web page"
        }]
        return buttons
    else:
        if info["top_element_style"] == "large":
            buttons = [{
                "type": "web_url",
                "url": info["data"][0]["url"],
                "title": "Web page"
            }]
            return buttons
        else:
            buttons = [{
                "type": "web_url",
                "url": "https://www.kkbox.com/tw/tc/search.php?word=" + info["token"],
                "title": "More"
            }]
            return buttons



# reply request
def reply_text(user_id, message):
    data = {
        "recipient": {"id": user_id},
        "message": {"text": message}
    }
    response = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=data)


def reply_greeting_message():
    data = {
        "setting_type": "greeting",
        "greeting": {
            "text": "請輸入\"/歌曲名稱\"\n或輸入\"#專輯名稱\"\n或輸入\"$歌單名稱\"\n或輸入\"@歌手名稱\""
        }
    }


def reply_image_url(user_id, image_url):
    data = {
        "recipient": {
            "id": user_id
        },
        "message": {
            "attachment": {
                "type": "image",
                "payload": {
                    "url": image_url
                }
            }
        }
    }
    response = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=data)
    print(response.content)


def reply_generic_template(user_id, info):
    element = produce_elements(info)
    data = {
        "recipient": {
            "id": user_id
        },
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "sharable": True,
                    "image_aspect_ratio": "square",
                    "elements": element
                }
            }
        }
    }
    response = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=data)
    print(response.content)


def reply_list_template(user_id, info):
    elements = produce_elements(info)
    buttons = produce_buttons(info)

    data = {
        "recipient": {
            "id": user_id
        },
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "list",
                    "top_element_style": info["top_element_style"],
                    "elements": elements,
                    "buttons": buttons
                }
            }
        }
    }

    response = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=data)
    print(response.content)
