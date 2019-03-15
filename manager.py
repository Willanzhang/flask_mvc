from application import manager
from flask_script import Server
from www import *

# web server
manager.add_command("runserver", Server(host='0.0.0.0', port=app.config['SERVER_PORT'], use_debugger=True))


def main():
    manager.run()


if __name__ == '__main__':
    try:
        import sys
        sys.exit(main())
    except Exception as e:
        import traceback
        traceback.print_exc()
    # 1、print_exc()：是对异常栈输出
    # 2、format_exc()：是把异常栈以字符串的形式返回，print(traceback.format_exc()) 就相当于traceback.print_exc()
    # 3、print_exception()：traceback.print_exc()实现方式就是traceback.print_exception(sys.exc_info())，可以点sys.exc_info() 进去看看实现
