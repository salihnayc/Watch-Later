DROP TABLE IF EXISTS channels;
DROP TABLE IF EXISTS videos;

CREATE TABLE channels
(id TEXT PRIMARY KEY, title TEXT NOT NULL, description TEXT NOT NULL);

CREATE TABLE videos 
(id TEXT PRIMARY KEY, title TEXT NOT NULL, channelId TEXT NOT NULL, description TEXT NOT NULL, duration TEXT NOT NULL,
FOREIGN KEY (channelId) REFERENCES channels(id));