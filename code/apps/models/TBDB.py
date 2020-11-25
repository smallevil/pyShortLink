# -*- coding: utf-8 -*-
# @Author: smallevil
# @Date:   2020-11-24 10:48:40
# @Last Modified by:   smallevil
# @Last Modified time: 2020-11-26 01:40:26

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

    def getUserInfoByID(self, userID):
        params = {'uid':userID}
        sql = "select * from user_info where user_id=:uid"
        rows = self._conn.query(sql, **params)
        row = rows.first(as_dict=True)
        if row:
            return row
        else:
            return None

    def updateUserPasswd(self, userID, passwd):
        params = {'uid':userID, 'passwd':passwd}
        sql = "update user_info set user_passwd=:passwd where user_id=:uid"
        self._conn.query(sql, **params)

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
    def addLinkInfo(self, domain, url, urlmd5, userID, tag):
        if not domain or not url or not urlmd5 or not userID:
            return None

        with self._db.transaction() as tx:
            params = {'tag':tag, 'domain':domain, 'url':url, 'urlmd5':urlmd5, 'uid':userID, 'ctime':str(arrow.now().format('YYYY-MM-DD HH:mm:ss'))}
            sql = "insert into link_info (link_tag, link_domain, link_url, link_url_md5, user_id, link_ctime) values (:tag, :domain, :url, :urlmd5, :uid, :ctime)"
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

        if self._dbType:
            if userID <= 0:
                params = {'start':start, 'limit':limit}
                sql = "select * from link_info order by link_id desc limit :start, :limit"
            else:
                params = {'uid':userID, 'start':start, 'limit':limit}
                sql = "select * from link_info where user_id=:uid order by link_id desc limit :start, :limit"
        else:
            if userID <= 0:
                params = {'start':start, 'limit':limit}
                sql = "select * from link_info order by link_id desc limit :limit offset :start"
            else:
                params = {'uid':userID, 'start':start, 'limit':limit}
                sql = "select * from link_info where user_id=:uid order by link_id desc limit :limit offset :start"

        info = {}
        rows = self._conn.query(sql, **params)
        info['list'] = rows.all(as_dict=True)

        if userID <= 0:
            sql = "select count(link_id) as total from link_info"
        else:
            sql = "select count(link_id) as total from link_info where user_id=:uid"
        rows = self._conn.query(sql, **params)
        row = rows.first(as_dict=True)
        info['total'] = row['total']

        return info

    def getOriginalUrlByKey(self, key):
        if not key:
            return None

        params = {'key':key}
        sql = "select * from link_info where link_key=:key"
        rows = self._conn.query(sql, **params)
        row = rows.first(as_dict=True)
        if row:
            return row['link_url']
        else:
            return None

    def addRecord(self, linkID, uaStr, uvStatus, uaType, referrer, platform, browser, device, userIP, country, province, city):
        if not linkID:
            return None

        country = country.decode('utf-8')
        province = province.decode('utf-8')
        city = city.decode('utf-8')
        params = {'link_id':int(linkID), 'ua':str(uaStr), 'uv_status':int(uvStatus), 'ua_type':uaType, 'referrer':str(referrer), 'platform':str(platform), 'browser':str(browser), 'device':str(device),  'ip':str(userIP), 'country':country, 'province':province, 'city':city, 'date':str(arrow.now().format('YYYY-MM-DD')), 'ctime':str(arrow.now().format('YYYY-MM-DD HH:mm:ss'))}
        sql = "insert into link_record (record_ua, record_referer, record_uv_status, record_ip, record_platform, record_browser, record_device, record_ua_type, record_country, record_province, record_city, link_id, record_date, record_ctime) values (:ua, :referrer, :uv_status, :ip, :platform, :browser, :device, :ua_type, :country, :province, :city, :link_id, :date, :ctime)"
        self._conn.query(sql, **params)


    #每日统计
    def statDay(self, linkID):
        endTime = arrow.now().format('YYYY-MM-DD HH:mm:00')
        startTime = arrow.now().shift(minutes=-5).format('YYYY-MM-DD HH:mm:00')

        params = {'linkID':linkID, 'start_time':startTime, 'end_time':endTime}
        sql = "select sum(record_id) as total from link_record where link_id=:linkID and record_ctime >=:start_time and record_ctime <=:end_time"
        rows = self._conn.query(sql, **params)
        row = rows.first(as_dict=True)
        if row['total']:
            pv = row['total']
        else:
            pv = 0

        params = {'linkID':linkID, 'start_time':startTime, 'end_time':endTime}
        sql = "select sum(record_id) as total from link_record where link_id=:linkID and record_ctime >=:start_time and record_ctime <=:end_time group by record_ip"
        rows = self._conn.query(sql, **params)
        row = rows.first(as_dict=True)
        if row:
            ip = row['total']
        else:
            ip = 0

        params = {'linkID':linkID, 'start_time':startTime, 'end_time':endTime}
        sql = "select sum(record_id) as total from link_record where link_id=:linkID and record_ctime >=:start_time and record_ctime <=:end_time and record_uv_status=0"
        rows = self._conn.query(sql, **params)
        row = rows.first(as_dict=True)
        if row['total'] >= 0:
            uv = row['total']
        else:
            uv = 0

        params = {'date':arrow.now().format('YYYY-MM-DD'), 'time':str(arrow.now().format('HH:mm:ss')), 'pv':pv, 'uv':uv, 'ip':ip, 'link_id':linkID}
        sql = "insert into link_stat (stat_day_pv, stat_day_uv, stat_day_ip, link_id, stat_date, stat_time) values (:pv, :uv, :ip, :link_id, :date, :time)"
        self._conn.query(sql, **params)






