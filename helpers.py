import requests
import os
from flask import make_response

def downloadThumbnail(url, name):
    try:
        response = requests.get(url)
        response.raise_for_status()

        with open(f"static/thumbnails/{name}.jpg", "wb") as file:
            file.write(response.content)

        return {
            "success": {
                "message": f"static/thumbnails/{name}.jpg"
            }
        }
    except requests.RequestException as e:
        return {
            "error": {
                "message": f"Request error: {e}"
            }
        }

def fetchVideo(id):
    url = f"https://youtube.googleapis.com/youtube/v3/videos?part=snippet,contentDetails&id={id}&key={os.getenv('KEY')}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data["pageInfo"]["totalResults"] == 0:
            return {
                "error": {
                    "message": "URL is not valid"
                }
            }

        downloadThumbnail(data["items"][0]["snippet"]["thumbnails"]["maxres"]["url"], data["items"][0]["id"])

        return {
            "id": data["items"][0]["id"],
            "title": data["items"][0]["snippet"]["title"],
            "channelId": data["items"][0]["snippet"]["channelId"],
            "description": data["items"][0]["snippet"]["description"],
            "duration": data["items"][0]["contentDetails"]["duration"]
        }
    except requests.RequestException as e:
        return {
            "error": {
                "message": f"Request error: {e}"
            }
        }


def fetchChannel(id):
    url = f"https://youtube.googleapis.com/youtube/v3/channels?part=snippet&id={id}&key={os.getenv('KEY')}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data["pageInfo"]["totalResults"] == 0:
            return {
                "error": {
                    "message": "URL is not valid"
                }
            }

        downloadThumbnail(data["items"][0]["snippet"]["thumbnails"]["high"]["url"], data["items"][0]["id"])
        return {
            "id": data["items"][0]["id"],
            "title": data["items"][0]["snippet"]["title"],
            "description": data["items"][0]["snippet"]["description"]
        }
    except requests.RequestException as e:
        return {
            "error": {
                "message": f"Request error: {e}"
            }
        }


def appendVideo(db, id):
    video = fetchVideo(id)
    if "error" in video:
        return video

    c = db.execute("SELECT * FROM channels WHERE id = ?", video["channelId"])
    if not c:
        channel = fetchChannel(video["channelId"])
        if "error" in channel:
            return channel
        
        db.execute("INSERT INTO channels VALUES (?, ?, ?)", 
                   channel["id"], channel["title"], channel["description"])
    
    db.execute("INSERT INTO videos VALUES (?, ?, ?, ?, ?)", 
                video["id"], video["title"], video["channelId"], video["description"], video["duration"])

    return {
        "videoId": video["id"],
        "videoTitle": video["title"],
        "videoDescription": video["description"],
        "duration": video["duration"],
        "channelId": channel["id"],
        "channelTitle": channel["title"],
        "channelDescription": channel["description"]
    }

def sendJson(json, code=200):
    response = make_response(json, code)
    response.headers["Content-Type"] = "application/json"
    return response
