# Facebook Messenger Chatbot
This is a messenger bot with KKBOX open API for searching songs, albums, playlist, artist data from KKBOX database
You can use it for chat with "[Innovation Chatbot](https://www.facebook.com/Innovation-Chatbot-122808158329830)" fans page on facebook

## Setup
This project is runnable on Heroku!

### Prerequisites

- [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
- [Facebook developers account](https://developers.facebook.com)
- [Heroku-Postgres-addon](https://elements.heroku.com/addons/heroku-postgresql)

### 1. Create a Heroku app and Heroku postgres addon

```
$ cd /path/to/fb-chatbots

$ heroku create

# HEROKU_APPID is given to you from the above command. Run `heroku apps` to list them all.
$ heroku addons:create heroku-postgresql --app {HEROKU_APPID}

# URL_TO_HEROKU_APP is the URL given to you from the above command
$ heroku config:set APP_URL='https://{URL_TO_HEROKU_APP}'
```

### 2. Connect to the github or push to Heroku git

you can choose one method to do 

### 3. Create a Facebook app

- go to [facebook developer](https://developers.facebook.com/apps) and sign in
- create a messanger app
- you need to choose at least message and messaging_postbacks events
    ![](https://i.imgur.com/TvIwEEu.png)

### 4. Get the Facebook fans page access token

- see Token Generation section
    ![](https://i.imgur.com/cGpgM4J.png)
- slect which fans page to connect the bot
- copy the page access token

### 5-1 Setup app webhook

- click webhooks
- click "edit subscription" button
    ![](https://i.imgur.com/yhcLPxu.png)
- set callback url with heroku app url
- set verify token
    ![](https://i.imgur.com/VM6xryF.png)

### 5-2. Set environment variable

you need to set

- ACCESS_TOKEN : fans page access token
- AUTHORIZATION : KKbox account authorization
- DATABASE_URL : your heroku postgres addon url
- VERIFY_TOKEN : what you set on verify token
- ADMIN_ID : administrator's conversation id
    ![](https://i.imgur.com/q4JDg9i.png)

### 6. Deploy the project on Heroku

## Usage
start chat with your fans page which set above on the messenger
```
    請輸入"/歌曲名稱"
    或輸入"#專輯名稱"
    或輸入"$歌單名稱"
    或輸入"@歌手名稱"
```

### 1. search track
input ``` /[TRACK_NAME] ```
<img src="https://i.imgur.com/s0a0fss.jpg" width="50%">
<img src="https://i.imgur.com/PVyjr10.jpg" width="50%">

### 2. search album
input ``` #[ALBUM_NAME] ```
<img src="https://i.imgur.com/P51z4or.png" width="50%">
<img src="https://i.imgur.com/YqJPnxf.png" width="50%">

### 3. search playlist
input ``` $[PLAYLIST_NAME] ```
<img src="https://i.imgur.com/4wGr3lT.jpg" width="50%">
<img src="https://i.imgur.com/ZwaeDQL.png" width="50%">

### 4. search artist
input ``` @[ARTIST_NAME] ```
<img src="https://i.imgur.com/YlPAYuI.png" width="50%">
<img src="https://i.imgur.com/rPw780i.png" width="50%">

### 5. broadcast
input ``` ![WHAT_YOU_WANT_TO_BROADCAST]```
> for only conversation id is ADMIN_ID 
> and only broadcast to conversation id is in database
