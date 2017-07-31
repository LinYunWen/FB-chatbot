# -*- coding: utf-8 -*-
# find_info (version before refactoring)





def get_song_id(json):
    return json["tracks"]["data"][0]["id"]


def get_album_id(json):
    return json["albums"]["data"][0]["id"]


def get_playlist_id(json):
    return json["playlists"]["data"][0]["id"]


def get_artist_id(json):
    return json["artists"]["data"][0]["id"]


def get_web_url(json, mode):
    if mode == InputType.TRACK:
        return json["tracks"]["data"][0]["url"]
    elif mode == InputType.ALBUM:
        return json["albums"]["data"][0]["url"]
    elif mode == InputType.PLAYLIST:
        return json["playlists"]["data"][0]["url"]


def get_widget_image(json, mode, index):
    if mode == InputType.TRACK:
        return json["tracks"]["data"][index]["album"]["images"][-1]["url"]
    elif mode == InputType.ALBUM:
        return json["albums"]["data"][index]["images"][-1]["url"]
    elif mode == InputType.PLAYLIST:
        return json["playlists"]["data"][index]["images"][-1]["url"]
    elif mode == InputType.ARTIST:
        return json["data"][index]["album"]["images"][-1]["url"]


def get_widget_name(json, mode, index):
    if mode == InputType.TRACK:
        return json["tracks"]["data"][index]["name"]
    elif mode == InputType.ALBUM:
        return json["albums"]["data"][index]["name"]
    elif mode == InputType.PLAYLIST:
        return json["playlists"]["data"][index]["title"]
    elif mode == InputType.ARTIST:
        return json["name"]
    
def artist_songs(id, territory):
    headers = {"Authorization": "Bearer FDP48nJQc7DJD9MJtkhVqA=="}
    return requests.get("https://api.kkbox.com/v1.1/artists/" + id + "/top-tracks?territory=" + territory + "&limit=5",
                        headers=headers).json()


def get_artist_info(json, index):
    name = json["artists"]["data"][index]["name"]
    url = json["artists"]["data"][index]["url"]
    image_url = json["artists"]["data"][index]["images"][1]["url"]
    return {"name": name, "url": url, "image_url": image_url}


def get_artist_name(mode, json):
    if mode == TRACK:
        return json["tracks"]["data"][0]["album"]["artist"]["name"]
    elif mode == ALBUM:
        return json["albums"]["data"][0]["artist"]["name"]
    return "error"


def get_alblum_name(mode, json):
    if mode == TRACK:
        return json["tracks"]["data"][0]["album"]["name"]
    elif mode == ALBUM:
        return json["albums"]["data"][0]["name"]
    return "error"




def find_info(token, mode):
    if mode == InputType.TRACK:
        song_json = search(token, "track", "TW")
        num = get_summary_total(song_json)
        if num > 0:
            if matching_result(token, song_json["tracks"]["data"][0]["name"]) or num == 1:
                song_id = get_song_id(song_json)
                print("id: ", song_id)
                widget_song_url = get_widget_song_url(song_id)

                return {
                    "mode": InputType.TRACK,
                    "response_type": ResponseType.SINGLE,
                    "subtitle": get_alblum_name(mode, song_json) + "   " + get_artist_name(mode, song_json),
                    "widget_song_url": widget_song_url,
                    "title": get_widget_name(song_json, mode, 0),
                    "widget_image_url": modify_image_size(get_widget_image(song_json, mode, 0), 400),
                    "web_url": get_web_url(song_json, mode)
                }
            # return {"mode":TRACK, "widget_song_url":widget_song_url, "web_title":web_title, "widget_image_url":widget_image_url}
            else:
                data = []
                for i in range(0, num):
                    song_id = song_json["tracks"]["data"][i]["id"]
                    widget_song_url = get_widget_song_url(song_id)
                    data.append({
                        "widget_song_url": widget_song_url,
                        "title": get_widget_name(song_json, mode, i),
                        "widget_image_url": get_widget_image(song_json, mode, i),
                        "subtitle": song_json["tracks"]["data"][i]["album"]["artist"]["name"]
                    })

                return {
                    "mode": InputType.TRACK,
                    "num": num,
                    "token": token,
                    "response_type": ResponseType.LIST,
                    "top_element_style": "compact",
                    "data": data
                }
        elif num == 0:
            return {"mode": ErrorType.NO_RESULT}

    elif mode == InputType.ALBUM:
        album_json = search(token, "album", "TW")
        num = get_summary_total(album_json)
        if num > 0:
            if matching_result(token, album_json["albums"]["data"][0]["name"]) or num == 1:
                album_id = get_album_id(album_json)
                print("id: ", album_id)
                widget_album_url = get_widget_album_url(album_id)

                return {
                    "mode": InputType.ALBUM,
                    "response_type": ResponseType.SINGLE,
                    "subtitle": get_artist_name(mode, album_json),
                    "widget_song_url": widget_album_url,
                    "title": get_widget_name(album_json, mode, 0),
                    "widget_image_url": modify_image_size(get_widget_image(album_json, mode, 0), 400),
                    "web_url": get_web_url(album_json, mode)
                }
            # return {"mode":ALBUM, "widget_song_url":widget_album_url, "web_title":web_title, "widget_image_url":widget_image_url}
            else:
                albums_data = []
                for i in range(0, num):
                    album_id = album_json["albums"]["data"][i]["id"]
                    widget_album_url = get_widget_album_url(album_id)
                    albums_data.append({
                        "widget_song_url": widget_album_url,
                        "title": get_widget_name(album_json, mode, i),
                        "widget_image_url": get_widget_image(album_json, mode, i),
                        "subtitle": album_json["albums"]["data"][i]["artist"]["name"]
                    })

                return {
                    "mode": InputType.ALBUM,
                    "num": num,
                    "token": token,
                    "response_type": ResponseType.LIST,
                    "top_element_style": "compact",
                    "data": album_data
                }
        else:
            return {"mode": ErrorType.NO_RESULT}
    elif mode == InputType.PLAYLIST:
        playlist_json = search(token, "playlist", "TW")
        num = get_summary_total(playlist_json)
        if num > 0:
            if matching_result(token, playlist_json["playlists"]["data"][0]["title"]) or num == 1:
                playlist_id = get_playlist_id(playlist_json)
                print("id: ", playlist_id)
                widget_playlist_url = get_widget_playlist_url(playlist_id)

                return {
                    "mode": InputType.PLAYLIST,
                    "response_type": ResponseType.SINGLE,
                    "subtitle": playlist_json["playlists"]["data"][0]["description"],
                    "widget_song_url": widget_playlist_url,
                    "title": get_widget_name(playlist_json, mode, 0),
                    "widget_image_url": modify_image_size(get_widget_image(playlist_json, mode, 0), 400),
                    "web_url": get_web_url(playlist_json, mode)
                }
            # return {"mode":PLAYLIST, "widget_song_url":widget_playlist_url, "web_title":web_title, "widget_image_url":widget_image_url}
            else:
                playlists_data = []
                for i in range(0, num):
                    playlist_id = playlist_json["playlists"]["data"][i]["id"]
                    widget_playlist_url = get_widget_playlist_url(playlist_id)
                    playlists_data.append({
                        "widget_song_url": widget_playlist_url,
                        "title": get_widget_name(playlist_json, mode, i),
                        "widget_image_url": get_widget_image(playlist_json, mode, i),
                        "subtitle": playlist_json["playlists"]["data"][i]["description"]
                    })

                return {
                    "mode": InputType.PLAYLIST,
                    "num": num,
                    "token": token,
                    "response_type": ResponseType.LIST,
                    "top_element_style": "compact",
                    "data": playlists_data
                }
        else:
            return {"mode": ErrorType.NO_RESULT}
    elif mode == InputType.ARTIST:
        artist_json = search(token, "artist", "TW")
        artist_num = get_summary_total(artist_json)
        if artist_num > 0:
            if matching_result(token, artist_json["artists"]["data"][0]["name"]) or artist_num == 1:
                artist_id = get_artist_id(artist_json)
                print("id: ", artist_id)

                songs_data = [get_artist_info(artist_json, 0)]
                song_json = artist_songs(artist_id, "TW")
                # print(song_json)
                if "error" in song_json:
                    return {"mode": ErrorType.NO_RESULT}

                song_num = get_summary_total(song_json)
                if song_num == 4:
                    song_num = 3

                for i in range(0, song_num):
                    song_id = song_json["data"][i]["id"]
                    widget_song_url = get_widget_song_url(song_id)
                    songs_data.append({
                        "widget_song_url": widget_song_url,
                        "title": get_widget_name(song_json["data"][i], mode, 0),
                        "subtitle": song_json["data"][i]["album"]["name"],
                        "widget_image_url": get_widget_image(song_json, mode, i)
                    })

                return {
                    "mode": InputType.ARTIST,
                    "num": song_num,
                    "response_type": ResponseType.LIST,
                    "top_element_style": "large",
                    "data": songs_data
                }
            else:
                artists_data = []
                for i in range(0, artist_num):
                    artist_id = artist_json["artists"]["data"][i]["id"]
                    artist_info = get_artist_info(artist_json, i)
                    artists_data.append({
                        "widget_song_url": artist_info["url"],
                        "title": artist_info["name"],
                        "widget_image_url": artist_info["image_url"],
                        "subtitle": artist_info["name"]
                    })

                return {
                    "mode": InputType.ARTIST,
                    "num": artist_num,
                    "token": token,
                    "response_type": ResponseType.LIST,
                    "top_element_style": "compact",
                    "data": artists_data
                }
        else:
            return {"mode": ErrorType.NO_RESULT}

    elif mode == InputType.INQUERY:
        return

