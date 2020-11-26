# -*- coding: utf-8 -*-
# @Author: smallevil
# @Date:   2020-11-24 10:48:40
# @Last Modified by:   smallevil
# @Last Modified time: 2020-11-26 12:37:53

import hashlib
from .TBDB import TBDB

class AdminModel(object):
    def __init__(self, dbURI):
        self._db = TBDB(dbURI)

    def getDB(self):
        return self._db

    #后台登录
    def adminLogin(self, nick, passwd):
        passwd = self.md5(passwd)
        info = self._db.getUserInfoByNickAndPasswd(nick, passwd)
        if not info:
            return None

        userInfo = {}
        userInfo['id'] = info['user_id']
        userInfo['nick'] = info['user_nick']
        userInfo['level'] = info['user_level']
        return userInfo

    def getUserInfoByID(self, userID):
        return self._db.getUserInfoByID(userID)

    #添加短链接
    def addLinkInfo(self, userID, url, domain, tag):
        urlmd5 = self.md5(url)
        info = self._db.getLinkInfoByMD5(userID, urlmd5)
        if info:
            return {'key':info['link_key']}

        ret = self._db.addLinkInfo(domain, url, urlmd5, userID, tag)
        if ret:
            return {'key':ret}
        else:
            return None

    #得到指定用户所有短链
    def getUrlsByUserID(self, userID, start, limit):
        return self._db.getUrlsByUserID(userID, start, limit)


    def md5(self, key):
        return hashlib.md5(key).hexdigest()


    #产生短链接key
    #此算法有问题,当不同用户超过4次对同一网址创建短链时无法成功
    def shortKeyForMD5(self, url):
        base32 = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
                   'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
                   'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
                   'y', 'z','0', '1', '2', '3', '4', '5'
                  ]

        hexStr = self.md5(url)
        hexStrLen = len(hexStr)
        subHexLen = hexStrLen / 8
        output = []
        for i in range(0,subHexLen):
            subHex = '0x'+hexStr[i*8:(i+1)*8]
            res = 0x3FFFFFFF & int(subHex,16)
            out = ''
            for j in range(6):
                val = 0x0000001F & res
                out += (base32[val])
                res = res >> 5
            output.append(out)
        return output


    #整理统计
    def setStatDay(self):
        start = 0
        limit = 10000
        while True:
            urls = self._db.getUrlsByUserID(0, start, limit)
            if not urls['list']:
                break

            start = start + limit

            for urlInfo in urls['list']:
                self._db.statDay(urlInfo['link_id'])


    def statPV(self, linkID, date):
        return self._db.statPV(linkID, date)

    def statPlatform(self, linkID, date):
        return self._db.statPlatform(linkID, date)

    def statBrowser(self, linkID, date):
        return self._db.statBrowser(linkID, date)

    def statAddr(self, linkID, date):
        return self._db.statAddr(linkID, date)


