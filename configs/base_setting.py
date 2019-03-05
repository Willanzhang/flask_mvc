SERVER_PORT = 9000
DEBUG = False
SQLALCHEMY_ECHO = False

AUTH_COOKIE_NAME="food"

# 过滤url
IGNORE_URLS = [
    "^/user/login"
]

IGNOER_CHECK_LOGIN_URL = [
    "^/static",
    "^/favicon.ico"
]
