from flask import Flask, request
import requests

app = Flask(__name__)

ACCESS_TOKEN = "EAAEtsX9w5Q0BAHz42VnrkeSNajWpvJjc8ONCs4plPKlBzoafvDTxTEkVY1gGmTxiDcPKauUVHmACxSoyJ715dwhuvRV78QZCWKrQNnACFevghRzjU33xWYFuwZChpDTsVpnSZCtKmZBayMzOzXFdiWly9OZAJPgjgptYzBZAnivwZDZD"


@app.route("/",methods=["GET"])
def handle_verification():
	return request.args['hub.challenge']


def reply(user_id,message):
	data = {
		"recipient": {"id": user_id},
		"message": {"text": message}
	}
	response = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=data)
	print("response: ",response.content)


@app.route("/",methods=["POST"])
def handle_incoming_message():
	data = request.json
	sender = data["entry"][0]["messaging"][0]["sender"]["id"]
	message = data["entry"][0]["messaging"][0]["message"]["text"]

	print("message: ",message)
	reply(sender,message)

	return "ok"


if __name__ == "__main__":
	app.run(debug=True)
