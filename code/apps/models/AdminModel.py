# -*- coding: utf-8 -*-
# @Author: smallevil
# @Date:   2020-11-24 10:48:40
# @Last Modified by:   smallevil
# @Last Modified time: 2020-11-24 15:50:29

import hashlib
from TBDB import *

class AdminModel(object):
    def __init__(self, dbURI):
        self._db = TBDB(dbURI)

    def getDB(self):
        return self._db

    #后台登录
    def adminLogin(self, nick, passwd):
        passwd = hashlib.md5(passwd).hexdigest()
        info = self._db.getUserInfoByNickAndPasswd(nick, passwd)
        if not info:
            return None

        userInfo = {}
        userInfo['id'] = info['user_id']
        userInfo['nick'] = info['user_nick']
        userInfo['level'] = info['user_level']
        return userInfo


