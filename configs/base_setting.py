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

API_IGNORE_URLS = [
    "^/api"
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
paykey 商户秘钥
mch_id 商户id
callback_url  微信的回调地址
'''
MINA_APP = {
    'appid': 'wxe3445334e3277c73',
    'appkey': 'e280d207de19a46caef2c1eb16e32bf5',
    'paykey': 'e2bbfbedda23',
    'mch_id': '1443337302',
    'callback_url': 'api/order/callback'
}


UPLOAD = {
    'ext': ['jpg', 'gif', 'bmp', 'jpeg', 'png'],
    'prefix_path': '/webs/static/upload/',
    'prefix_url': '/static/upload/'
}

APP = {
    'domain': 'http://127.0.0.1:5000'
}

PAY_STATUS_DISPLAY_MAPPING = {
    '0': "订单关闭",
    '1': "支付成功",
    '-8': "待支付",
    '-7': "待发货",
    '-6': "待确认",
    '-5': "待评价"
}
