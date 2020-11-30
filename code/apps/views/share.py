# -*- coding: utf-8 -*-
# @Author: smallevil
# @Date:   2020-11-24 10:48:40
# @Last Modified by:   smallevil
# @Last Modified time: 2020-11-30 21:17:11

import arrow, urllib
from flask import Blueprint, render_template, redirect, session, request, make_response, current_app
from ..models.AdminModel import AdminModel
import math, urllib, arrow, json
from datetime import timedelta
from hashids import Hashids

share = Blueprint('share', __name__, url_prefix='/s')


@share.route('/statpv/key/<key>', defaults={'date': ''}, methods=['GET'])
@share.route('/statpv/key/<key>/date/<date>', methods=['GET'])
def shareStatPV(key, date):
    if not date:
        date = str(arrow.now().format('YYYYMMDD'))

    try:
        hashids = Hashids(min_length=8, salt=current_app.config['SHARE_URL_SALT'])
        linkID, limitDate = hashids.decode(key)
    except:
        return redirect('/error?msg=' + urllib.quote('非法操作'))

    if int(date) > int(limitDate):
        return redirect('/error?msg=' + urllib.quote('此统计共享已到期'))


    model = AdminModel(current_app.config['DATABASE_URI'])
    linkInfo = model.getLinkInfoByID(linkID)
    if not linkInfo:
        return redirect('/error?msg=' + urllib.quote('非法操作'))

    rets = {'link_id':linkID, 'key':key, 'title':linkInfo['link_tag'], 'limit_date':str(arrow.get(str(limitDate), 'YYYYMMDD').format('YYYY-MM-DD')), 'list':[]}
    #rets['list'] = model.statPV(linkID, date)
    rets['date'] = date
    rets['date1'] = str(arrow.now().format('YYYYMMDD'))
    rets['date7'] = str(arrow.now().shift(days=-7).format('YYYYMMDD'))
    rets['date30'] = str(arrow.now().shift(days=-30).format('YYYYMMDD'))
    rets['link_info'] = linkInfo

    datas = {}
    for info in model.statPV(linkID, date):
        if date == rets['date1']:
            t = str(info['time'])
        else:
            t = str(info['date'])

        datas[t] = {'pv': int(info['pv']), 'uv':int(info['uv']), 'ip':int(info['ip'])}


    def datetime_range(start, end, delta):
        current = start
        while current < end:
            yield current
            current += delta

    if date == rets['date1']:
        limitDates = [dt.format('HH:mm:ss') for dt in
           datetime_range(arrow.now().floor('day'), arrow.now().ceil('day'),
           timedelta(minutes=5))]
    else:
        limitDates = [str(dt.format('YYYY-MM-DD')) for dt in
           datetime_range(arrow.get(date, 'YYYYMMDD'), arrow.now(),
           timedelta(days=1))]

    times = []
    pvs = []
    uvs = []
    ips = []

    for cTime in limitDates:
        times.append(cTime)
        if cTime in datas.keys():
            pvs.append(datas[cTime]['pv'])
            uvs.append(datas[cTime]['uv'])
            ips.append(datas[cTime]['ip'])
        else:
            pvs.append(0)
            uvs.append(0)
            ips.append(0)

    return render_template('/share/stat_pv.html', tplData=rets, times=times, pvs=pvs, uvs=uvs, ips=ips)


@share.route('/statplatform/key/<key>', defaults={'date': ''}, methods=['GET'])
@share.route('/statplatform/key/<key>/date/<date>', methods=['GET'])
def shareStatPlatform(key, date):
    if not date:
        date = str(arrow.now().format('YYYYMMDD'))

    try:
        hashids = Hashids(min_length=8, salt=current_app.config['SHARE_URL_SALT'])
        linkID, limitDate = hashids.decode(key)
    except:
        return redirect('/error?msg=' + urllib.quote('非法操作'))

    if int(date) > int(limitDate):
        return redirect('/error?msg=' + urllib.quote('此统计共享已到期'))

    model = AdminModel(current_app.config['DATABASE_URI'])
    linkInfo = model.getLinkInfoByID(linkID)
    if not linkInfo:
        return redirect('/error?msg=' + urllib.quote('非法操作'))

    rets = {'link_id':linkID, 'key':key, 'title':linkInfo['link_tag'], 'limit_date':str(arrow.get(str(limitDate), 'YYYYMMDD').format('YYYY-MM-DD')), 'link_info':linkInfo, 'list':[]}
    #rets['list'] = model.statPlatform(linkID, date)
    rets['date'] = date
    rets['date1'] = str(arrow.now().format('YYYYMMDD'))
    rets['date7'] = str(arrow.now().shift(days=-7).format('YYYYMMDD'))
    rets['date30'] = str(arrow.now().shift(days=-30).format('YYYYMMDD'))

    charts = {'legend_data':[], 'series_data':[]}
    for info in model.statPlatform(linkID, date):
        charts['legend_data'].append(info['platform'] + ': ' + str(info['total']))

        t = {}
        t['name'] = info['platform'] + ': ' + str(info['total'])
        t['value'] = info['total']
        charts['series_data'].append(t)
        del t

    return render_template('/share/stat_platform.html', tplData=rets, charts=charts)


@share.route('/statbrowser/key/<key>', defaults={'date': ''}, methods=['GET'])
@share.route('/statbrowser/key/<key>/date/<date>', methods=['GET'])
def shareStatBrowser(key, date):
    if not date:
        date = str(arrow.now().format('YYYYMMDD'))

    try:
        hashids = Hashids(min_length=8, salt=current_app.config['SHARE_URL_SALT'])
        linkID, limitDate = hashids.decode(key)
    except:
        return redirect('/error?msg=' + urllib.quote('非法操作'))

    if int(date) > int(limitDate):
        return redirect('/error?msg=' + urllib.quote('此统计共享已到期'))

    model = AdminModel(current_app.config['DATABASE_URI'])
    linkInfo = model.getLinkInfoByID(linkID)
    if not linkInfo:
        return redirect('/error?msg=' + urllib.quote('非法操作'))

    rets = {'link_id':linkID, 'key':key, 'title':linkInfo['link_tag'], 'limit_date':str(arrow.get(str(limitDate), 'YYYYMMDD').format('YYYY-MM-DD')), 'link_info':linkInfo, 'list':[]}
    #rets['list'] = model.statBrowser(linkID, date)
    rets['date'] = date
    rets['date1'] = str(arrow.now().format('YYYYMMDD'))
    rets['date7'] = str(arrow.now().shift(days=-7).format('YYYYMMDD'))
    rets['date30'] = str(arrow.now().shift(days=-30).format('YYYYMMDD'))

    charts = {'legend_data':[], 'series_data':[]}
    for info in model.statBrowser(linkID, date):
        charts['legend_data'].append(info['browser'] + ': ' + str(info['total']))

        t = {}
        t['name'] = info['browser'] + ': ' + str(info['total'])
        t['value'] = info['total']
        charts['series_data'].append(t)
        del t

    return render_template('/share/stat_browser.html', tplData=rets, charts=charts)


@share.route('/stataddr/key/<key>', defaults={'date': ''}, methods=['GET'])
@share.route('/stataddr/key/<key>/date/<date>', methods=['GET'])
def shareStatAddr(key, date):
    if not date:
        date = str(arrow.now().format('YYYYMMDD'))

    try:
        hashids = Hashids(min_length=8, salt=current_app.config['SHARE_URL_SALT'])
        linkID, limitDate = hashids.decode(key)
    except:
        return redirect('/error?msg=' + urllib.quote('非法操作'))

    if int(date) > int(limitDate):
        return redirect('/error?msg=' + urllib.quote('此统计共享已到期'))

    model = AdminModel(current_app.config['DATABASE_URI'])
    linkInfo = model.getLinkInfoByID(linkID)
    if not linkInfo:
        return redirect('/error?msg=' + urllib.quote('非法操作'))

    rets = {'link_id':linkID, 'key':key, 'title':linkInfo['link_tag'], 'limit_date':str(arrow.get(str(limitDate), 'YYYYMMDD').format('YYYY-MM-DD')), 'link_info':linkInfo, 'list':[]}
    #rets['list'] = model.statAddr(linkID, date)
    rets['date'] = date
    rets['date1'] = str(arrow.now().format('YYYYMMDD'))
    rets['date7'] = str(arrow.now().shift(days=-7).format('YYYYMMDD'))
    rets['date30'] = str(arrow.now().shift(days=-30).format('YYYYMMDD'))

    charts = {'legend_data':[], 'series_data':[]}
    for info in model.statAddr(linkID, date):
        charts['legend_data'].append(info['address'] + ': ' + str(info['total']))

        t = {}
        t['name'] = info['address'] + ': ' + str(info['total'])
        t['value'] = info['total']
        charts['series_data'].append(t)
        del t

    return render_template('/share/stat_addr.html', tplData=rets, charts=charts)