from cs50 import SQL
from dotenv import load_dotenv
from helpers import fetchVideo, fetchChannel

load_dotenv()

db = SQL("sqlite:///watch.db")

ids = ["DiKc3ypdU90", "6FU4YahMa5s", "NyfIf6qQjLA", "FvR7pT9jWcg", "lfT__wKnoQA"]

for id in ids:
    video = fetchVideo(id)
    if "error" in video:
        print(video)
        continue

    c = db.execute("SELECT * FROM channels WHERE id = ?", video["channelId"])
    if not c:
        channel = fetchChannel(video["channelId"])
        if "error" in channel:
                print(channel)
                continue
    
        db.execute("INSERT INTO channels VALUES (?, ?)", channel["id"], channel["title"])

    db.execute("INSERT INTO videos VALUES (?, ?, ?, ?, ?)", 
               video["id"], video["title"], video["channelId"], video["description"], video["duration"])
