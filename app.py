from flask import Flask, render_template, request, make_response
from urllib.parse import urlsplit, parse_qs

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

videos = [
        {
            "thumbnail": "todo",
            "title": "Example Video",
            "channel": "Example Channel",
            "description": "Example Description",
            "duration": "todo" 
        },
        {
            "thumbnail": "todo",
            "title": "Example Video 2",
            "channel": "Example Channel 2",
            "description": "Example Description 2",
            "duration": "todo"
        }
    ]

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

@app.route("/api/list")
def list():
    response = make_response(videos)
    response.headers["Content-Type"] = "application/json"
    return response


@app.route("/api/add", methods=["POST"])
def add():
    url = request.form.get("url")
    if not url:
        message = {"error": {"message": "URL is required"}}
        response = make_response(message,400)
        response.headers["Content-Type"] = "application/json"
        return response

    u = urlsplit(url)
    print(u)
    if u.scheme != "https":
        message = {"error": {"message": "URL is not valid"}}
        response = make_response(message,400)
        response.headers["Content-Type"] = "application/json"
        return response

    if u.netloc in ["www.youtube.com", "youtube.com"]:
        q = parse_qs(u.query)
        return q["v"]
    elif u.netloc == "youtu.be":
        return u.path
    else:
        message = {"error": {"message": "URL is not valid"}}
        response = make_response(message,400)
        response.headers["Content-Type"] = "application/json"
        return response