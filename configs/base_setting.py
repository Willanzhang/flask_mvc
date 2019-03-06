SERVER_PORT = 9000
DEBUG = False
SQLALCHEMY_ECHO = False

AUTH_COOKIE_NAME="food"

# 过滤url
IGNORE_URLS = [
    "^/user/login",
    "^/api"
]

IGNOER_CHECK_LOGIN_URL = [
    "^/static",
    "^/favicon.ico"
]

'''
分页配置
'''
PAGE_SIZE = 50
PAGE_DISPLAY = 10

'''
搜索变量
'''
STATUS_MAPPING = {
    "1": "正常",
    "0": "已删除"
}

'''
小程序配置
'''
MINA_APP = {
    'appid': 'wxe3445334e3277c73',
    'appkey': 'e280d207de19a46caef2c1eb16e32bf5'
}
