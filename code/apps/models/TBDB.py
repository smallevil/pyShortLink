# -*- coding: utf-8 -*-
# @Author: smallevil
# @Date:   2020-11-24 10:48:40
# @Last Modified by:   smallevil
# @Last Modified time: 2020-11-24 20:55:49

import records

class TBDB(object):
    def __init__(self, dbURI):
        self._db = records.Database(dbURI)
        self._conn = self._db.get_connection()

    #根据昵称和密码得到信息
    def getUserInfoByNickAndPasswd(self, nick, passwd):

        if not nick or not passwd:
            return None

        params = {"nick":nick, "passwd":passwd}
        sql = "select * from user_info where user_nick=:nick and user_passwd=:passwd"
        rows = self._conn.query(sql, **params)
        row = rows.first(as_dict=True)
        if row:
            return row
        else:
            return None

    #根据key得到短链信息
    def getLinkInfoByKey(self, key):
        if not key:
            return None

        params = {'key':key}
        sql = "select * from link_info where link_key=:key"
        rows = self._conn.query(sql, **params)
        row = rows.first(as_dict=True)
        if row:
            return row
        else:
            return None

    #根据urlmd5判断是否已添加
    def getLinkInfoByMD5(self, userID, urlmd5):
        if not urlmd5 or not userID:
            return None

        params = {'uid':userID, 'md5':urlmd5}
        sql = "select * from link_info where user_id=:uid and link_url_md5=:md5"
        rows = self._conn.query(sql, **params)
        row = rows.first(as_dict=True)
        if row:
            return row
        else:
            return None

    #添加短链
    def addLinkInfo(self, key, url, urlmd5, userID):
        if not key or not url or not urlmd5 or not userID:
            return None

        params = {'key':key, 'url':url, 'urlmd5':urlmd5, 'uid':userID}
        sql = "insert into link_info (link_key, link_url, link_url_md5, user_id) values (:key, :url, :urlmd5, :uid)"
        try:
            row = self._conn.query(sql, **params)
            return True
        except:
            return False






