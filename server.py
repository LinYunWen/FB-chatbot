from flask import Flask, request
from pymessenger.bot import Bot
from bs4 import BeautifulSoup
import requests
import os

app = Flask(__name__)

#this is a token to match FB fans page
#Light up
ACCESS_TOKEN = "EAAEtsX9w5Q0BAHz42VnrkeSNajWpvJjc8ONCs4plPKlBzoafvDTxTEkVY1gGmTxiDcPKauUVHmACxSoyJ715dwhuvRV78QZCWKrQNnACFevghRzjU33xWYFuwZChpDTsVpnSZCtKmZBayMzOzXFdiWly9OZAJPgjgptYzBZAnivwZDZD"
#test bot
#ACCESS_TOKEN = "EAACMTV0RjhoBADvhR8S2ZAw905cbZCQWZAFIAWYIl9JLw5Snqz6XSL2dqeSE6gP8kB3uW9iqJb7CAfiooqAdo5qXxZBIRWGvCL7rVXZBq3wkohaKX6HZBa3iuFq6Rpk55iiODQOpzX1VVupSWzqYXJfLkFfDn6QOkt3RIEAglLiAZDZD"
bot = Bot(ACCESS_TOKEN)

SONG = 0
ALBUM = 1
PLAYLIST = 2
ARTIST = 3

#for verify
@app.route("/", methods=["GET"])
def handle_verification():
	if request.args["hub.verify_token"] == "test_for_verify":
		return request.args["hub.challenge"]
	else:
		return "Wrong Verify Token"

def get_access_token():
	return 0

#get web page
def get_web_page(url):
	response = requests.get(url)

	response.encoding = 'utf-8'
	if response.status_code != 200:
		print("Invalid url: ", response.url)
		return -1
	else:
		return response.text

def parse_web_html(doc):
	return BeautifulSoup(doc, "html.parser")
def get_web_title(soup):
	return soup.head.title

#reply request
def reply_text(user_id, message):
	data = {
		"recipient": {"id": user_id},
		"message": {"text": message}
	}
	response = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=data)

def reply_image_url(user_id, image_url):
	data = {
		"recipient":{
			"id":user_id
		},
		"message":{
			"attachment":{
				"type":"image",
				"payload":{
					"url":image_url
				}
			}
		}
	}
	response = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=data)
	print(response.content)




def reply_generic_template(user_id, info):
	"""
	data = {
		"recipient":{
			"id":user_id
		},
		"message":{
			"attachment":{
				"type":"template",
				"payload":{
					"template_type":"open_graph",
					"elements":[
						{
							"url":widget_url,
							"buttons":[
								{
									"type":"web_url",
									"url":"https://www.google.com.tw/",
									"title":"Listen entity song"
								}
							]
						}
					]
				}
			}
		}
	}
	"""
	data = {
		"recipient":{
			"id":user_id
		},
		"message":{
			"attachment":{
				"type":"template",
				"payload":{
					"template_type":"generic",
					"sharable":True,
					"image_aspect_ratio":"square",
					"elements":[
						{
							"title":info["web_title"],
							"image_url":info["widget_image_url"],
							"default_action":{
								"type":"web_url",
								"url":info["widget_song_url"],
								"webview_height_ratio":"tall"
							},
							"buttons":[
								{
									"type":"web_url",
									"url":"https://www.google.com.tw/",
									"title":"Listen entity song"
								}
							]
						}
					]
				}
			}
		}
	}
	response = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=data)
	print(response.content)


def reply_list_template(user_id, info):
	data = {
		"recipient":{
			"id":user_id
		},
		"message":{
			"attachment":{
				"type":"template",
				"payload":{
					"template_type":"list",
					"top_element_style":"large",
					"sharable":True,
					"elements":[
						{
							"title":info[0]["name"],
							"image_url":info[0]["image_url"],
							"default_action":{
								"type":"web_url",
								"url":info[0]["url"],
								"webview_height_ratio":"compact"
							}
						},
						{
							"title":info[1]["web_title"],
							"image_url":info[1]["widget_image_url"],
							"default_action":{
								"type":"web_url",
								"url":info[1]["widget_song_url"],
								"webview_height_ratio":"compact"
							}
						},
						{
							"title":info[2]["web_title"],
							"image_url":info[2]["widget_image_url"],
							"default_action":{
								"type":"web_url",
								"url":info[2]["widget_song_url"],
								"webview_height_ratio":"compact"
							}
						},
						{
							"title":info[3]["web_title"],
							"image_url":info[3]["widget_image_url"],
							"default_action":{
								"type":"web_url",
								"url":info[3]["widget_song_url"],
								"webview_height_ratio":"compact"
							}
						}
					],
					"buttons":[
						{
							"type":"web_url",
							"url":"https://www.google.com.tw/",
							"title":"More"
						}
					]				
				}
			}
		}
	}
	response = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=data)
	print(response.content)

def test(user_id):
	"""generic template
	data = {
		"recipient":{
			"id":"USER_ID"
		},
		"message":{
			"attachment":{
				"type":"template",
				"payload":{
					"template_type":"generic",
					"elements":[
						{
							"title":"Welcome to Peter\'s Hats",
							"image_url":"https://petersfancybrownhats.com/company_image.png",
							"subtitle":"We\'ve got the right hat for everyone.",
							"default_action": {
								"type": "web_url",
								"url": "https://peterssendreceiveapp.ngrok.io/view?item=103",
								"messenger_extensions": True,
								"webview_height_ratio": "tall",
								"fallback_url": "https://peterssendreceiveapp.ngrok.io/"
							},
							"buttons":[
								{
									"type":"web_url",
									"url":"https://petersfancybrownhats.com",
									"title":"View Website"
								},{
									"type":"postback",
									"title":"Start Chatting",
									"payload":"DEVELOPER_DEFINED_PAYLOAD"
								}              
							]      
						}
					]
				}
			}
		}
	}
	"""
	#"""open graph template
	data = {
		"recipient":{
			"id":user_id
		},
		"message":{
			"attachment":{
				"type":"template",
				"payload":{
					"template_type":"open_graph",
					"elements":[
						{
							"url":"https://widget.kkbox.com/v1/?id=8sD5pE4dV0Zqmmler6&type=song",
							"buttons":[
								{
									"type":"web_url",
									"url":"https://en.wikipedia.org/wiki/Rickrolling",
									"title":"View More"
								}              
							]      
						}
					]
				}
			}
		}
	}
	#"""
	response = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=data)
	print(response.content)


def set_sender_action(user_id, action):
	data = {
		"recipient":{
			"id":user_id
		},
		"sender_action":action
	}
	response = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=data)
	#print(response.content)

def handle_error_request(user_id, error_type):
	if error_type==-1:
		reply_text(user_id,"未設定之指令")
		reply_text(user_id,"請輸入\"/歌曲歌曲\"\n或輸入\"#專輯名稱\"\n或\"輸入$歌單名稱\"\n或\"輸入@歌手名稱\"")
	
	return 0

def search(inquiry, type, territory):
	payload = {"q": inquiry, "type": type, "territory": territory}
	headers = {"Authorization": "Bearer FDP48nJQc7DJD9MJtkhVqA=="}
	
	response = requests.get("https://api.kkbox.com/v1.1/search", params=payload, headers=headers)
	#print("content: ",response.json())
	#print("url: ",response.url)
	return response.json()

def artist_songs(id, territory):
	headers = {"Authorization": "Bearer FDP48nJQc7DJD9MJtkhVqA=="}
	return requests.get("https://api.kkbox.com/v1.1/artists/" + id + "/top-tracks?territory=" + territory + "&limit=5", headers=headers).json()

def get_artist_info(json):
	name = json["artists"]["data"][0]["name"]
	url = json["artists"]["data"][0]["url"]
	image_url = json["artists"]["data"][0]["images"][1]["url"]
	return {"name":name, "url":url, "image_url":image_url}

def parse_request(message):
	song_index = message.find("聽")
	
	if message[0] == '/':
		return {"mode":SONG, "token":message[1:]}
	elif message[0] == '#':
		return {"mode":ALBUM, "token":message[1:]}
	elif message[0] == '$':
		return {"mode":PLAYLIST, "token":message[1:]}
	elif message[0] == '@':
		return {"mode":ARTIST, "token":message[1:]}

	if song_index<0:
		return {"mode":-1}
	else:
		return {"mode":SONG, "token":message[song_index:]}

def find_info(token, mode):

	if mode == SONG:
		song_json = search(token,"track","TW")
		song_id = get_song_id(song_json)
		print("id: ", song_id)
	
		widget_song_url = get_widget_song_url(song_id)
		web_page = get_web_page(widget_song_url);
		soup = parse_web_html(web_page)
		web_title = get_web_title(soup).text
		widget_style_value = soup.find("div",{"class":"widget-cover clickable"})["style"]
		widget_image_url = widget_style_value[widget_style_value.find("(")+1:widget_style_value.find(")")]

		print("image url: ", widget_image_url)
		print("title: ", web_title)

		return {"widget_song_url":widget_song_url, "web_title":web_title, "widget_image_url":widget_image_url}
	elif mode == ALBUM:
		album_json = search(token,"album","TW")
		album_id = get_album_id(album_json)
		print("id: ",album_id)

		widget_album_url = get_widget_album_url(album_id)
		web_page = get_web_page(widget_album_url);
		soup = parse_web_html(web_page)
		web_title = get_web_title(soup).text
		widget_style_value = soup.find("div",{"class":"widget-cover clickable"})["style"]
		widget_image_url = widget_style_value[widget_style_value.find("(")+1:widget_style_value.find(")")]

		print("image url: ", widget_image_url)
		print("title: ", web_title)

		return {"widget_song_url":widget_album_url, "web_title":web_title, "widget_image_url":widget_image_url}
	elif mode == PLAYLIST:
		playlist_json = search(token,"playlist","TW")
		playlist_id = get_playlist_id(playlist_json)
		print("id: ",playlist_id)

		widget_playlist_url = get_widget_playlist_url(playlist_id)
		web_page = get_web_page(widget_playlist_url);
		soup = parse_web_html(web_page)
		web_title = get_web_title(soup).text
		widget_style_value = soup.find("div",{"class":"widget-cover clickable"})["style"]
		widget_image_url = widget_style_value[widget_style_value.find("(")+1:widget_style_value.find(")")]

		print("image url: ", widget_image_url)
		print("title: ", web_title)

		return {"widget_song_url":widget_playlist_url, "web_title":web_title, "widget_image_url":widget_image_url}
	elif mode == ARTIST:
		artist_json = search(token,"artist","TW")
		artist_id = get_artist_id(artist_json)
		print("id: ",artist_id)

		songs_data = [get_artist_info(artist_json)]
		song_json = artist_songs(artist_id,"TW")
		for i in range(0,3):
			song_id = song_json["data"][i]["id"]

			widget_song_url = get_widget_song_url(song_id)
			web_page = get_web_page(widget_song_url);
			soup = parse_web_html(web_page)
			web_title = get_web_title(soup).text
			widget_style_value = soup.find("div",{"class":"widget-cover clickable"})["style"]
			widget_image_url = widget_style_value[widget_style_value.find("(")+1:widget_style_value.find(")")]

			print("image url: ", widget_image_url)
			print("title: ", web_title)
			
			songs_data.append({"widget_song_url":widget_song_url, "web_title":web_title, "widget_image_url":widget_image_url})

		return songs_data

def get_song_id(json):
	return json["tracks"]["data"][0]["id"]
def get_album_id(json):
	return json["albums"]["data"][0]["id"]
def get_playlist_id(json):
	return json["playlists"]["data"][0]["id"]
def get_artist_id(json):
	return json["artists"]["data"][0]["id"]

def get_widget_song_url(id):
	return "https://widget.kkbox.com/v1/?id=" + id + "&type=song"
def get_widget_album_url(id):
	return "https://widget.kkbox.com/v1/?id=" + id + "&type=album"
def get_widget_playlist_url(id):
	return "https://widget.kkbox.com/v1/?id=" + id + "&type=playlist"

def reply(user_id, info, mode):

	set_sender_action(user_id,"mark_seen")
	set_sender_action(user_id,"typing_on")
	
	#test
	#test(user_id)
	#reply_text(user_id,'https://widget.kkbox.com/v1/?id=4qtXcj31wYJTRZbb23&type=album')

	#send text
	#reply_text(user_id,"https://www.google.com")

	#send image
	#reply_image_url(user_id,"http://pansci.asia/wp-content/uploads/2013/08/71a868311.jpg")
	#bot.send_image_url(user_id,"http://pansci.asia/wp-content/uploads/2013/08/71a868311.jpg")

	#send attachment 
	#bot.send_attachment_url(user_id,"template","https://widget.kkbox.com/v1/?id=8sD5pE4dV0Zqmmler6&type=song")
	if mode == ARTIST:
		reply_list_template(user_id,info)
	elif mode >= 0:
		reply_generic_template(user_id,info)
		#reply_list_template(user_id,info)
	

@app.route("/",methods=["POST"])
def handle_incoming_message():
	data = request.json
	sender = data["entry"][0]["messaging"][0]["sender"]["id"]
	text = data["entry"][0]["messaging"][0]["message"]["text"]

	print("message: ",text)
	request_token = parse_request(text)
	if request_token["mode"]<0:
		handle_error_request(sender,request_token["mode"])
	else:
		info = find_info(request_token["token"],request_token["mode"])
		reply(sender,info,request_token["mode"])

	return "ok"


if __name__ == "__main__":
	app.run(debug=True)
