import requests

from . import utils
from .post import Post

class Client:

    def __init__(self, username, api_key):

        self.username = username
        self.api_key = api_key

        self.session = requests.Session()
        self.session.headers.update({
            "Ieddit-Username": self.username,
            "Ieddit-Api-Key": self.api_key
        })

    def post(self, *args, **kwargs):
        return self.session.post(*args, **kwargs)

    def get(self, *args, **kwargs):
        return self.session.get(*args, **kwargs)

    def create_post(self, title, sub, url = "", text = "", anonymous = False):
        return Post.create(self, title, sub, url, text, anonymous)