# -*- coding: utf-8 -*-
# @Author: smallevil
# @Date:   2020-11-24 10:48:40
# @Last Modified by:   smallevil
# @Last Modified time: 2020-11-26 12:37:50

from user_agents import parse
from .TBDB import TBDB

class FrontModel(object):
    def __init__(self, dbURI):
        self._db = TBDB(dbURI)

    def getDB(self):
        return self._db

    #得到原始网址
    def getLinkInfoByKey(self, key):
        linkInfo = self._db.getLinkInfoByKey(key)
        return linkInfo

    #添加记录
    def addViewRecord(self, linkID, uaStr, uvStatus, referrer, userIP, address):
        ua = parse(uaStr)

        if ua.is_bot:
            platform = 'Bot'
        else:
            if ua.os.family.find('Mac') >= 0:
                platform = 'Mac'
            elif ua.os.family.find('Win') >= 0:
                platform = 'Win'
            else:
                platform = ua.os.family

        browser = ua.browser.family.replace('Mobile', '').strip()
        device = ua.device.family

        if uaStr.lower().find('micromessenger') >= 0:
            browser = '微信'
        elif uaStr.lower().find('qq') >= 0:
            if uaStr.lower().find('mqqbrowser') >= 0:
                browser = 'QQ浏览器'
            else:
                browser = 'QQ'
        elif uaStr.lower().find('alipay') >= 0:
            browser = '支付宝'
        elif uaStr.lower().find('weibo') >= 0:
            browser = '微博'

        uaType = 0
        if ua.is_mobile:
            uaType = 4
        elif ua.is_tablet:
            uaType = 3
        elif ua.is_pc:
            uaType = 2
        elif ua.is_bot:
            uaType = 1

        self._db.addRecord(linkID, uaStr, uvStatus, uaType, referrer, platform, browser, device, userIP, address['country'], address['province'], address['city'])





