说明文档
===============
[预览地址](https://m.zhangbowen.club/)
暂未设置游客账户
===============
##项目说明
-----
+ 使用python flask 项目做的订餐系统
+ 数据mysql 作为数据库 redis 作为简单数据缓存
+ 整个项目包括 后台管理系统， 小程序前台页面   所有接口编写， 以及对接微信小程序 登录 支付（虚假商户id, 只是保证整个流程，注册商户即可使用） app 正再使用Flutter开发中
+ 使用jobs定时更新订单状态
+ 定时持久化数据库核心数据

ptyhon的运行环境管理使用 virtualenvwrapper 进行管理


##启动
* Mac: export ops_config=local|production && python manage.py runserver
* Win: set ops_config=local|production  && python manage.py runserver

启动脚本
```
  1 #!/bin/sh
  2 # start flask_mvc
  3 export ops_config=production
  4 source /usr/bin/virtualenvwrapper.sh
  5 cd /data/www/flask_mvc
  6 workon flask_pri
  7 uwsgi --ini uwsgi.ini
```

##


![prelook](https://m.zhangbowen.club/static/upload/20190804/6ce6fb91993b492ea2f8e57eb36d3123.png "prelook")

