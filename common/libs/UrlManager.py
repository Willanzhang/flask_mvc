# -*- coding: utf-8 -*-

import datetime
class UrlManager(object):
    def __init__(self):
        pass

    @staticmethod
    def buildUrl( path ):
        return path

    @staticmethod
    def buildStaticUrl(path):
        ver = "%s" % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        path = "/static" + path + "?ver=" + ver
        return UrlManager.buildUrl(path)
