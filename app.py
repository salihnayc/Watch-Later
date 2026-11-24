from cs50 import SQL
from helpers import fetchVideo, sendJson, appendVideo
from flask import Flask, render_template, request, make_response
from urllib.parse import urlsplit, parse_qs
import os

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

db = SQL("sqlite:///watch.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/details/<id>")
def details(id):
    return render_template("details.html")

@app.route("/api/videos")
def list():
    videos = db.execute("SELECT videos.id as videoId, videos.title as videoTitle, videos.description as videoDescription, videos.duration as videoDuration, channels.id as channelId, channels.title as channelTitle FROM videos JOIN channels ON videos.channelId = channels.id")
    for v in videos:
        v["videoThumbnail"] = f"/static/thumbnails/{v["videoId"]}.jpg"
        v["channelLogo"] = f"/static/thumbnails/{v["channelId"]}.jpg"
        v["videoUrl"] = f"https://youtu.be/{v["videoId"]}"
        v["channelUrl"] = f"https://www.youtube.com/channel/{v["channelId"]}"

    return sendJson(videos)

@app.route("/api/video/<id>")
def video(id):
    video = db.execute("SELECT videos.id as videoId, videos.title as videoTitle, videos.description as videoDescription, videos.duration as videoDuration, channels.id as channelId, channels.title as channelTitle FROM videos JOIN channels ON videos.channelId = channels.id WHERE videos.id = ?", id)
    if not video:
        message = {"error": {"message": f"Video {id} is not found"}}
        return sendJson(message, 404)
    
    video[0]["videoThumbnail"] = f"/static/thumbnails/{video[0]["videoId"]}.jpg"
    video[0]["channelLogo"] = f"/static/thumbnails/{video[0]["channelId"]}.jpg"
    video[0]["videoUrl"] = f"https://youtu.be/{video[0]["videoId"]}"
    video[0]["channelUrl"] = f"https://www.youtube.com/channel/{video[0]["channelId"]}"

    return sendJson(video[0])

@app.route("/api/add", methods=["POST"])
def add():
    url = request.form.get("url")
    if not url:
        message = {"error": {"message": "URL is required"}}
        return sendJson(message,400)

    u = urlsplit(url)
    if u.scheme != "https":
        message = {"error": {"message": "URL is not valid"}}
        return sendJson(message,400)

    if u.netloc in ["www.youtube.com", "youtube.com"]:
        q = parse_qs(u.query)
        result = appendVideo(db, q["v"][0])

        if not "error" in result:
            return sendJson(result)
        
        return sendJson(result, 400)
    
    elif u.netloc == "youtu.be":
        result = appendVideo(db, u.path.replace("/", ""))

        if not "error" in result:
            return sendJson(result, 201)

        return sendJson(result, 400)
    
    else:
        message = {"error": {"message": "URL is not valid"}}
        return sendJson(message,400)

@app.route("/api/remove", methods=["DELETE"])
def remove():
    id = request.form.get("id")
    if not id:
        message = {"error": {"message": "id is required"}}
        return sendJson(message,400)

    deleted = db.execute("DELETE FROM videos WHERE id=?",id)
    if deleted:
        # Remove thumbnail
        try:
            os.remove(f"static/thumbnails/{id}.jpg")
        except FileNotFoundError:
            print(f"Cannot remove 'static/thumbnails/{id}.jpg': Doesn't exists.")

        # Remove unnecessary channels if any
        unnecessary = db.execute("SELECT id FROM channels WHERE id NOT IN (SELECT channelId FROM videos)")
        if unnecessary:
            db.execute("DELETE FROM channels WHERE id= ?", unnecessary[0]["id"])
            try:
                os.remove(f"static/thumbnails/{unnecessary[0]["id"]}.jpg")
            except FileNotFoundError:
                print(f"Cannot remove 'static/thumbnails/{unnecessary[0]["id"]}.jpg': Doesn't exists.")
        
        message = {"success": {"message": f"video {id} deleted"}}
        return sendJson(message)
    else:
        message = {"error": {"message": f"video {id} is not found"}}
        return sendJson(message, 404)
    