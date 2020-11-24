# -*- coding: utf-8 -*-
# @Author: smallevil
# @Date:   2020-11-24 10:48:40
# @Last Modified by:   smallevil
# @Last Modified time: 2020-11-24 15:38:36

import records

class TBDB(object):
    def __init__(self, dbURI):
        self._db = records.Database(dbURI)
        self._conn = self._db.get_connection()

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


