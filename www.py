# 所有路由都在这里注入
# from application import app
'''
统计拦截器
'''
from webs.interceptors.AuthInterceptor import *
from webs.interceptors.ApiAuthInterceptor import *

'''
蓝图功能 对所有url进行配置
'''
from webs.controllers.index import route_index
from webs.controllers.user.User import route_user
from webs.controllers.static import route_static
from webs.controllers.chart import route_chart
from webs.controllers.account.Account import route_account
from webs.controllers.finance.Finance import route_finance
from webs.controllers.food.Food import route_food
from webs.controllers.member.Member import route_member
from webs.controllers.stat.Stat import route_stat
from webs.controllers.api import route_api
from webs.controllers.upload.Upload import route_upload
from webs.controllers.stat.Stat import route_stat


app.register_blueprint(route_index, url_prefix="/")
app.register_blueprint(route_user, url_prefix="/user")
app.register_blueprint(route_static, url_prefix="/static")
app.register_blueprint(route_chart, url_prefix="/chart")
app.register_blueprint(route_account, url_prefix="/account")
app.register_blueprint(route_finance, url_prefix="/finance")
app.register_blueprint(route_food, url_prefix="/food")
app.register_blueprint(route_member, url_prefix="/member")
app.register_blueprint(route_stat, url_prefix="/stat")
app.register_blueprint(route_api, url_prefix="/api")
app.register_blueprint(route_upload, url_prefix="/upload")
app.register_blueprint(route_stat, url_prefix="/stat")
