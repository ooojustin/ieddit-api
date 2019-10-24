from .utils import API
from bs4 import BeautifulSoup
from dateutil import parser
import re, json

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
        if response.status_code != 200:
            raise Exception("Invalid status code from API [{}]".format(response.status_code))
            
        # load json response data
        data = json.loads(response.text)

        # create post object and set variables
        post = cls()
        for key, value in data.items():
            if key == "created":
                setattr(post, key, parser.parse(value))
            else:
                setattr(post, key, value)

        return post

    def __init__(self):
        pass
