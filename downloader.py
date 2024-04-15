import datetime
import os

import requests
from urllib.parse import urlparse

import helpers
from constants import TOKEN, OUT_DIR, GROUP_ID, API_VERSION, ALBUMS


res = requests.get("https://api.vk.com/method/photos.getAlbums", {
        "owner_id": GROUP_ID,
        "album_ids": ",".join(map(str, ALBUMS)),
        "v": API_VERSION,
        "access_token": TOKEN,
    })
albums = res.json()["response"]["items"]


for album in albums:
    date_created = datetime.datetime.fromtimestamp(album["created"])
    album_name = "[{date}] - {title}".format(date=date_created.strftime("%d.%m.%Y"), title=album["title"])

    album_dir = os.path.join(OUT_DIR, album_name)
    if not os.path.exists(album_dir):
        os.mkdir(album_dir)

    print(f'Processing album "{album_name}"...')

    params = {
        "owner_id": GROUP_ID,
        "album_id": album["id"],
        "v": API_VERSION,
        "access_token": TOKEN,
        "count": 1000
    }
    res = requests.get("https://api.vk.com/method/photos.get", params).json()

    for photo in res["response"]["items"]:
        max_size = max(photo["sizes"], key=lambda s: s["width"] + s["height"])
        photo_url = max_size["url"]

        filename = urlparse(photo_url).path.split("/")[-1]
        filename = os.path.join(album_dir, filename)
        if not os.path.exists(filename):
            helpers.download_file(photo_url, filename)
        else:
            print("[Warning] Skip photo {} in album {} file already exists".format(photo["id"],
                                                                                    photo["album_id"]))

