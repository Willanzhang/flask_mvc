# -*- coding: utf-8 -*-

# from application import app
import application

import datetime


class UrlManager(object):
    def __init__(self):
        pass

    @staticmethod
    def buildUrl(path):
        return path

    @staticmethod
    def buildStaticUrl(path):
        ver = "%s" % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        path = "/static" + path + "?ver=" + ver
        return UrlManager.buildUrl(path)

    @staticmethod
    def buildImageUrl(path):
        # url = ''
        app_config = application.app.config
        url = app_config['APP']['domain'] + app_config['UPLOAD']['prefix_url'] + path
        return url
