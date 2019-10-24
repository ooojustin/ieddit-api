import os, sys
from urllib.parse import urljoin

API = lambda e: urljoin("https://ieddit.com/api/", e)

LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(sys.modules['__main__'].__file__)), "__logs__")
if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)
