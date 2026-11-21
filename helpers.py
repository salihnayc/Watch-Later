import requests
import os
from flask import make_response

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
        return {
            "thumbnail": "todo",
            "title": data["items"][0]["snippet"]["title"],
            "channel": data["items"][0]["snippet"]["channelTitle"],
            "description": data["items"][0]["snippet"]["description"],
            "duration": data["items"][0]["contentDetails"]["duration"]
        }
    except requests.RequestException as e:
        return {
            "error": {
                "message": f"Request error: {e}"
            }
        }

def sendJson(json, code=200):
    response = make_response(json, code)
    response.headers["Content-Type"] = "application/json"
    return response
