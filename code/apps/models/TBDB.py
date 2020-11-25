# -*- coding: utf-8 -*-
# @Author: smallevil
# @Date:   2020-11-24 10:48:40
# @Last Modified by:   smallevil
# @Last Modified time: 2020-11-25 13:31:32

import records
from hashids import Hashids
import arrow

class TBDB(object):
    def __init__(self, dbURI):
        self._db = records.Database(dbURI)

        self._dbType = 1    #默认mysql
        if dbURI[0:6] == 'sqlite':
            self._dbType = 0
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
    def addLinkInfo(self, domain, url, urlmd5, userID):
        if not domain or not url or not urlmd5 or not userID:
            return None

        with self._db.transaction() as tx:
            params = {'domain':domain, 'url':url, 'urlmd5':urlmd5, 'uid':userID, 'ctime':str(arrow.now().format('YYYY-MM-DD HH:mm:ss'))}
            sql = "insert into link_info (link_domain, link_url, link_url_md5, user_id, link_ctime) values (:domain, :url, :urlmd5, :uid, :ctime)"
            tx.query(sql, **params)
            if self._dbType:
                sql = "select last_insert_id() as last_id"
            else:
                sql = "select last_insert_rowid() as last_id"
            rows = tx.query(sql)
            row = rows.first(as_dict=True)
            lastID = row['last_id']

            hashids = Hashids(min_length=4, alphabet='abcdefghijkmnpqrstuvwxyzABCDEFGHJKMNPQRSTUVWXYZ23456789')
            key = hashids.encode(lastID)

            params = {'key':key, 'last_id':lastID}
            sql = "update link_info set link_key=:key where link_id=:last_id"
            tx.query(sql, **params)
            return key

        return None

    def getUrlsByUserID(self, userID, start, limit):
        if not userID:
            return None

        params = {'uid':userID, 'start':start, 'limit':limit}
        if self._dbType:
            sql = "select * from link_info where user_id=:uid order by link_id desc limit :start, :limit"
        else:
            sql = "select * from link_info where user_id=:uid order by link_id desc limit :limit offset :start"

        info = {}
        rows = self._conn.query(sql, **params)
        info['list'] = rows.all(as_dict=True)

        sql = "select count(link_id) as total from link_info where user_id=:uid"
        rows = self._conn.query(sql, **params)
        row = rows.first(as_dict=True)
        info['total'] = row['total']

        return info







