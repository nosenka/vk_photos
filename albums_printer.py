import datetime
import os

import requests
from urllib.parse import urlparse

import helpers
from constants import TOKEN, OUT_DIR, GROUP_ID, API_VERSION



out_html = "<html><body>"

res = requests.get("https://api.vk.com/method/photos.getAlbums", {
        "owner_id": GROUP_ID,
        "v": API_VERSION,
        "access_token": TOKEN,
        "need_covers": 1,
        "count": 1000
    })
albums = res.json()["response"]["items"]
albums = sorted(albums, key=lambda a: a["created"], reverse=True)


for album in albums:
    date_created = datetime.datetime.fromtimestamp(album["created"])
    album_name = album["title"]
    thumb_url = album["thumb_src"]
    album_id = album["id"]
    album_link = f"https://vk.com/album{GROUP_ID}_{album_id}"

    out_html += f"<p>{date_created}</p>"
    out_html += f'<p><a href="{album_link}">{album_name}</a></p>'
    out_html += f"<p>ID: {album_id}</p>"
    out_html += f'<img src="{thumb_url}">'
    out_html += "<hr>"

out_html += "</html></body>"
print(out_html)
