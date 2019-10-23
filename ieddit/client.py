from ._2captcha import _2Captcha
import requests

from . import utils
from .post import Post

class Client:

    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0"

    def __init__(self, username, password, _2captcha_api_key = None, do_login = True):

        self.username = username
        self.password = password
        self.logged_in = False

        self._2captcha = _2Captcha(_2captcha_api_key) if _2captcha_api_key else None

        self.session = requests.Session()
        self.session.headers.update({"User-Agent": Client.USER_AGENT})

        if do_login:
            self.login()

    def _require_login(func):
        def wrapper(self, *args, **kwargs):
            if not self.logged_in:
                raise Exception(func.__name__ + " requires client to be authenticated.")
            return func(self, *args, **kwargs)
        return wrapper

    def login(self):
        
        params = {
            "username": self.username,
            "password": self.password
        }

        response = self.session.get(utils.IEDDIT("/login/"))
        response = self.session.post(utils.IEDDIT("/login/"), params)
        cookies = self.session.cookies.get_dict()

        if response.status_code != 200:
            raise Exception("ieddit returned unexpected status code [{}]".format(response.status_code))

        if response.url.endswith("/login/"):
            raise Exception("login failed :(\n" + response.text)

        self.logged_in = True

    @_require_login
    def create_post(self, title, sub, url = "", text = "", is_nsfw = False, is_anon = False):
        return Post.create(self, title, sub, url, text, is_nsfw, is_anon)