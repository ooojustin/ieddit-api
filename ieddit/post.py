from .utils import API
from bs4 import BeautifulSoup
from datetime import datetime
import re

class Post:

    @classmethod
    def create(cls, client, title, sub, url, text, anonymous):
        
        # establish parameters to post to server
        params = {
            "title": title,
            "sub": sub,
            "url": url,
            "self_text": text
        }

        # handle anonymous posts
        if anonymous:
            params["anonymous"] = True

        # send post request
        response = client.post(API("new_post"), params)     
        print(response.status_code, response.text)
            
        # create post object and set variables
        # post = cls()
        # post.id = post_id
        # post.full_url = post_url
        # post.client = client
        # post.title = title
        # post.sub = sub
        # post.url = url
        # post.text = text
        # post.is_nsfw = is_nsfw
        # post.is_anon = is_anon

        # return post

    def __init__(self):
        pass
