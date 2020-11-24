# -*- coding: utf-8 -*-
# @Author: smallevil
# @Date:   2020-11-24 10:48:40
# @Last Modified by:   smallevil
# @Last Modified time: 2020-11-24 21:05:58

import hashlib
from TBDB import *

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

    #添加短链接
    def addLinkInfo(self, userID, url):
        urlmd5 = self.md5(url)
        info = self._db.getLinkInfoByMD5(userID, urlmd5)
        if info:
            return {'key':info['link_key']}

        linkKeys = self.shortKey(url)

        for linkKey in linkKeys:
            if not self._db.getLinkInfoByKey(linkKey):
                self._db.addLinkInfo(linkKey, url, urlmd5, userID)
                return {'key':linkKey}

        return None

    def md5(self, key):
        return hashlib.md5(key).hexdigest()

    #产生短链接key
    #此算法有问题,当不同用户超过4次对同一网址创建短链时无法成功
    def shortKey(self, url):
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


