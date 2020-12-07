import hashlib
import time
import random

from httprunner import __version__


def get_httprunner_version():
    return __version__


def sum_two(m, n):
    return m + n


def sleep(n_secs):
    time.sleep(n_secs)

def get_token(phone,password,timestamp):
    s = "".join([phone,password,str(timestamp)])
    token = hashlib.md5(s.encode("utf-8")).hexdigest()
    print(f"token:{token}")
    return token

def get_member_id():
    return "7506370717891848"

def get_random_title():
    return f"demo-{random.randint(1,1000)}"

def gen_doc_title(num):
    return [get_random_title() for _ in range(num)]

