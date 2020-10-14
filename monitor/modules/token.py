import time
from django.utils import timezone
from github import Github
from utils.redistool import RS

BASE_URL = "https://api.github.com"


def get_available_token():
    for key in RS.keys():
        key = key.decode()
        if key.startswith('token'):
            reset = RS.hget(key, 'reset').decode()
            if not reset or (float(reset) + 28800) < timezone.now().timestamp():
                return key.split(':')[1]
    return None


def new_session():
    while True:
        token = get_available_token()
        if token:
            github_user = Github(
                base_url=BASE_URL,
                login_or_token=token
            )
            return github_user, token
        time.sleep(1)


def reset_token(github_user, token):
    rate_limit = github_user.get_rate_limit()
    reset_time = rate_limit.search.reset.timestamp()
    RS.hset('token:%s' % token, 'reset', reset_time)
    return new_session()
