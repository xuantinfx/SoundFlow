from . import ServiceAdapter
from .utils import decode_html
import os
import json
import requests

class YoutubeAdapter(ServiceAdapter):
    def __init__(self, key: str):
        self.search_api = f"https://www.googleapis.com/youtube/v3/search?part=snippet&order=relevance&maxResults=50&key={key}"
        self.name = "youtube"

    def search(self, query: str, type_: str):
        url = f"{self.search_api}&type={type_}&q={query}"
        resp = requests.get(url=url)
        json = resp.json()
        result = []
        for item in json["items"]:
            entry = {}
            entry["title"] = decode_html(item["snippet"]["title"])
            entry["author"] = decode_html(item["snippet"]["channelTitle"])
            entry["thumbnail_url"] = item["snippet"]["thumbnails"]["default"]["url"]
            entry["url"] = f"https://youtube.com/watch?v={item['id']['videoId']}"
            result.append(entry)
        return result

    def search_tracks(self, query: str):
        return self.search(query, 'video')
