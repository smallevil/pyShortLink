# -*- coding: utf-8 -*-
# @Author: smallevil
# @Date:   2020-11-24 10:48:40
# @Last Modified by:   smallevil
# @Last Modified time: 2020-11-25 22:43:36

import arrow
import geoip2.database
from ..models.ip2Region import Ip2Region
from flask import Blueprint, render_template, redirect, session, request, make_response, current_app
from ..models.FrontModel import FrontModel

front = Blueprint('front', __name__)

@front.route('/')
def webIndex():
    return ''


@front.route('/favicon.ico')
def fav():
    return ''

#前台404
@front.route('/error')
def frontError():
    msg = '出错啦!'
    if len(request.args.get('msg')) > 0:
        msg = request.args.get('msg')

    return render_template('/error.html', msg=msg)


#前台首页
@front.route('/<key>')
def frontIndex(key):
    model = FrontModel(current_app.config['DATABASE_URI'])
    linkInfo = model.getLinkInfoByKey(key)
    if not linkInfo:
        return redirect('/error?msg=访问出错')

    if linkInfo['link_status'] == -1:
        return redirect('/error?msg=你所访问的链接有风险')

    url = linkInfo['link_url']

    ua = request.headers.get("User-Agent")
    referrer = request.referrer
    if not referrer:
        referrer = ''

    userIP = request.headers.get('X-Forwarded-For')
    if not userIP:
        userIP = request.remote_addr

    uvStatus = 1
    resp = make_response()
    resp.headers['location'] = url
    uv = request.cookies.get('uv_' + key)
    if not uv:
        uvStatus = 0
        exTime = arrow.get(arrow.now().format("YYYY-MM-DD 23:59:59")).timestamp
        resp.set_cookie('uv_' + key, '1', expires=exTime)

    #计算IP地址位置
    address = getAddressByIP(userIP)


    model.addViewRecord(linkInfo['link_id'], ua, uvStatus, referrer, userIP, address)
    return resp, 302


def getAddressByIP(ip):
    try:
        address = getAddressFromGEO(ip)
        if address['country'] == '中国':
            address = getAddressFromRegion(ip)
    except:
        address = getAddressFromRegion(ip)

    return address


def getAddressFromGEO(ip):
    address = {'country':'other', 'province':'other', 'city':'other'}
    reader = geoip2.database.Reader(current_app.config['IP_GEO_FILE'])
    geoResult = reader.city(ip)

    address['country'] = geoResult.country.name
    try:
        address['address'] = geoResult.country.names['zh-CN']
    except:
        pass

    if geoResult.subdivisions.most_specific.name:
        address['province'] = geoResult.subdivisions.most_specific.name
        try:
            address['province'] = geoResult.subdivisions.most_specific.names['zh-CN']
        except:
            pass

    if geoResult.city.name:
        address['city'] = geoResult.city.name
        try:
            address['city'] = geoResult.city.names['zh-CN']
        except:
            pass

    return address


def getAddressFromRegion(ip):
    address = {'country':'other', 'province':'other', 'city':'other'}
    searcher = Ip2Region(current_app.config['IP_REGION_FILE'])
    data = searcher.memorySearch(ip)['region'].split('|')
    if len(data) >= 1:
        address['country'] = data[0]
    if len(data) >= 3:
        address['province'] = data[2]
    if len(data) >= 4:
        address['city'] = data[3]

    return address