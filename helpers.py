import requests
import os
from flask import make_response

# Downloads the thumbnail
def downloadThumbnail(url, name):
    try:
        # Make the request
        response = requests.get(url)
        response.raise_for_status()

        # Save to disk
        with open(f"static/thumbnails/{name}.jpg", "wb") as file:
            file.write(response.content)

        # Operation is succesful
        return {
            "success": {
                "message": f"static/thumbnails/{name}.jpg"
            }
        }
    # Error handling
    except requests.RequestException as e:
        return {
            "error": {
                "message": f"Request error: {e}"
            }
        }

# Fetches video data from id
def fetchVideo(id):
    # Build the url
    url = f"https://youtube.googleapis.com/youtube/v3/videos?part=snippet,contentDetails&id={id}&key={os.getenv('KEY')}"
    try:
        # Make the request
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # There is nothing returned for that id
        if data["pageInfo"]["totalResults"] == 0:
            return {
                "error": {
                    "message": "URL is not valid"
                }
            }

        # Download video's thumbnail
        downloadThumbnail(data["items"][0]["snippet"]["thumbnails"]["maxres"]["url"], data["items"][0]["id"])

        # Return the video data
        return {
            "id": data["items"][0]["id"],
            "title": data["items"][0]["snippet"]["title"],
            "channelId": data["items"][0]["snippet"]["channelId"],
            "description": data["items"][0]["snippet"]["description"],
            "duration": data["items"][0]["contentDetails"]["duration"]
        }
    # Error handling
    except requests.RequestException as e:
        return {
            "error": {
                "message": f"Request error: {e}"
            }
        }

# Fetches channel data from id
def fetchChannel(id):
    # Build the url
    url = f"https://youtube.googleapis.com/youtube/v3/channels?part=snippet&id={id}&key={os.getenv('KEY')}"

    try:
        # Make the response
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # There is nothing returned for that id
        if data["pageInfo"]["totalResults"] == 0:
            return {
                "error": {
                    "message": "URL is not valid"
                }
            }

        # Download channel's thumbnail
        downloadThumbnail(data["items"][0]["snippet"]["thumbnails"]["high"]["url"], data["items"][0]["id"])

        # Return the channel data
        return {
            "id": data["items"][0]["id"],
            "title": data["items"][0]["snippet"]["title"]
        }
    # Error handling
    except requests.RequestException as e:
        return {
            "error": {
                "message": f"Request error: {e}"
            }
        }

# Playlist items doesn't return video duration
# Just take the video ids
def fetchPlaylist(id):
    url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=contentDetails&playlistId={id}&maxResults=50&key={os.getenv("KEY")}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

         # There is nothing returned for that id
        if data["pageInfo"]["totalResults"] == 0:
            return {
                "error": {
                    "message": "URL is not valid"
                }
            }

        # select video ids
        ids = []
        for i in data["items"]:
            ids.append(i["contentDetails"]["videoId"])

        return ids
    
    except requests.RequestException as e:
        return {
            "error": {
                "message": f"Request error: {e}"
            }
        }

def appendVideo(db, id):
    # Fetch the video
    video = fetchVideo(id)
    if "error" in video:
        return video

    # Look for video's channel. If not exists in database add
    c = db.execute("SELECT * FROM channels WHERE id = ?", video["channelId"])
    if not c:
        channel = fetchChannel(video["channelId"])
        if "error" in channel:
            return channel
        
        db.execute("INSERT INTO channels VALUES (?, ?)", 
                   channel["id"], channel["title"])
    else:
        channel = {
            "id": c[0]["id"],
            "title": c[0]["title"]
        }

    # Try adding the video to database
    try:
        db.execute("INSERT INTO videos VALUES (?, ?, ?, ?, ?)", 
                    video["id"], video["title"], video["channelId"], video["description"], video["duration"])
    # Probably video already exists
    except ValueError:
        return {
            "error": {"message": f"Video '{video["title"]}' already exists."}
        }

    # Return the added video
    return {
        "videoId": video["id"],
        "videoTitle": video["title"],
        "videoDescription": video["description"],
        "videoDuration": video["duration"],
        "channelId": channel["id"],
        "channelTitle": channel["title"],
        "videoThumbnail":f"/static/thumbnails/{video["id"]}.jpg",
        "channelLogo": f"/static/thumbnails/{channel["id"]}.jpg",
        "videoUrl": f"https://youtu.be/{video["id"]}",
        "channelUrl": f"https://www.youtube.com/channel/{channel["id"]}"
    }

def appendPlaylist(db, id):
    # Get the video ids from playlist
    video_ids = fetchPlaylist(id)
    if "error" in video_ids:
        return video_ids

    videos = []

    # Cycle through ids if is it already exists skip the iteration
    for i in video_ids:
        v = appendVideo(db, i)
        if "error" in v:
            if "already exists" in v["error"]["message"]:
                continue
            else:
                return v
        videos.append(v)

    return videos

# A small function for sending json responses
def sendJson(json, code=200):
    response = make_response(json, code)
    response.headers["Content-Type"] = "application/json"
    return response
