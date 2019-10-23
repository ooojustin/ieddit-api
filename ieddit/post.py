from . import utils
from bs4 import BeautifulSoup
from datetime import datetime
import re

class Post:

    @classmethod
    def create(cls, client, title, sub, url = "", text = "", is_nsfw = False):
        
        # send get request and create html parser
        response = client.session.get(utils.IEDDIT("/create_post"))
        parser = BeautifulSoup(response.text, "html.parser")

        # determine request parameters
        params = {
            "url": url,
            "self_post_text": text,
            "title": title,
            "sub": sub,
        }

        # if 2captcha key was provided, find base64 captcha data and solve
        if client._2captcha:
            img = parser.select_one(".captcha-div img")
            base64 = img["src"].split()[1]       
            params["captcha"] = client._2captcha.solve(base64)
            if not params["captcha"]:
                raise Exception("failed to solve captcha :(")

        response = client.session.post(utils.IEDDIT("/create_post"), params)

        # retry if the captcha failed
        if "invalid captcha" in response.text:
            return cls.create(client, title, sub, url, text, is_nsfw)

        post_url, post_id = response.url, -1
        pattern = r"\/i\/{}\/(\d+)\/".format(sub)
        match = re.search(pattern, post_url)

        if match:
            # created post successfully!
            post_id = int(match.group(1))
        else:
            # failed to create post
            log_file_name = "create_post " + datetime.now().strftime("%Y-%m-%d %I-%m-%S %p").lower() + ".txt"
            log_file_path = os.path.join(client.LOG_DIR, log_file_name)
            with open(log_file_path, "w") as log_file:
                log_file.write(response.text)
            raise Exception("failed to create post: [{}]".format(response.status_code))
        
        # mark post as nsfw
        if is_nsfw:
            params = { "post_id": post_id }
            client.session.post(utils.IEDDIT("/user/nsfw"), params)
            
        # create post object and set variables
        post = cls()
        post.id = post_id
        post.full_url = post_url
        post.client = client
        post.title = title
        post.sub = sub
        post.url = url
        post.text = text
        post.is_nsfw = is_nsfw

        return post

    def __init__(self):
        pass
