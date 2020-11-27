# -*- coding: utf-8 -*-
# @Author: smallevil
# @Date:   2020-11-24 10:48:40
# @Last Modified by:   smallevil
# @Last Modified time: 2020-11-28 00:51:43

from flask import Blueprint, render_template, redirect, session, request, current_app
import functools
from ..models.AdminModel import AdminModel
import math, urllib, arrow, json

admin = Blueprint('admin', __name__, url_prefix='/admin')

def isLogin(func):
    @functools.wraps(func) # 修饰内层函数，防止当前装饰器去修改被装饰函数的属性
    def inner(*args, **kwargs):
        # 从session获取用户信息，如果有，则用户已登录，否则没有登录
        uid = session.get('uid')
        un = session.get('un')
        level = session.get('level')
        if not uid or not un or not level:
            return redirect('/admin/login') #没有登录就跳转到登录路由下
        else:
            # 已经登录的话 g变量保存用户信息，相当于flask程序的全局变量
            return func(*args, **kwargs)
    return inner


#后台登录
@admin.route('/login', methods=['GET', 'POST'])
def adminLogin():
    session.clear()
    if request.method == 'POST':
        nick = request.form.get('nick')
        passwd = request.form.get('passwd')
        if not nick or not passwd:
            return redirect('/admin/login')

        model = AdminModel(current_app.config['DATABASE_URI'])
        userInfo = model.adminLogin(nick, passwd)
        if userInfo:
            session['uid'] = userInfo['id']
            session['un'] = userInfo['nick']
            session['level'] = userInfo['level']
            return redirect('/admin/main')
        else:
            return redirect('/admin/login')


    return render_template('/admin/login.html')


#后台首页
@admin.route('/', methods=['GET'])
@isLogin
def adminIndex():
    return redirect('/admin/main')


#后台首页
@admin.route('/error', methods=['GET'])
def adminError():
    msg = '出错啦!'
    if len(request.args.get('msg')) > 0:
        msg = urllib.unquote(request.args.get('msg'))

    return render_template('/admin/error.html', msg=msg)


#后台退出页
@admin.route('/logout', methods=['GET', 'POST'])
@isLogin
def adminLogout():
    session.clear()
    return redirect('/admin/')


#后台欢迎页
@admin.route('/main', methods=['GET'])
@isLogin
def adminMain():
    return render_template('/admin/main.html')

#个人中心
@admin.route('/profile', methods=['GET', 'POST'])
@isLogin
def adminProfile():
    if request.method == 'POST':
        oldPasswd = request.form.get('old_passwd')
        newPasswd = request.form.get('new_passwd')
        renewPasswd = request.form.get('renew_passwd')

        if newPasswd != renewPasswd:
            return redirect('/error?msg=' + urllib.quote('两次输入密码不一样'))

        if oldPasswd == newPasswd:
            return redirect('/error?msg=' + urllib.quote('新密码不能与老密码相同'))

        model = AdminModel(current_app.config['DATABASE_URI'])
        userInfo = model.getUserInfoByID(session['uid'])
        if not userInfo:
            session.clear()
            return redirect('/error?msg=' + urllib.quote('异常退出'))

        if model.md5(oldPasswd) != userInfo['user_passwd']:
            return redirect('/error?msg=' + urllib.quote('旧密码错误'))

        model.getDB().updateUserPasswd(session['uid'], model.md5(newPasswd))
        return redirect('/admin/logout')
    else:
        return render_template('/admin/profile.html')

#添加短链
@admin.route('/add', methods=['GET', 'POST'])
@isLogin
def adminAdd():
    if request.method == 'POST':
        url = request.form.get('url')
        if url[0:4] != 'http':
            return redirect('/error?msg=' + urllib.quote('链接格式错误'))

        domain = request.form.get('domain')
        tag = request.form.get('tag')
        if url and domain and tag:
            model = AdminModel(current_app.config['DATABASE_URI'])
            ret = model.addLinkInfo(session.get('uid'), url, domain, tag)
            if ret:
                return redirect('/admin/urls/page/1')
        else:
            return redirect('/error?msg=' + urllib.quote('所有选项必填'))

        return redirect('/admin/add')

    return render_template('/admin/add.html')


#所有链接
@admin.route('/urls/page/<int:page>', methods=['GET'])
@isLogin
def adminUrls(page):
    if not page:
        page = 1

    if page < 1:
        page = 1

    limit = 10
    start = (page - 1) * limit

    model = AdminModel(current_app.config['DATABASE_URI'])
    ret = model.getUrlsByUserID(session.get('uid'), start, limit)

    #以下简化模板判断
    totalPage = math.ceil(ret['total'] / (limit * 1.0))

    minPage = page - 2
    if page - 2 < 1:
        minPage = 1
        maxPage = 5
    else:
        maxPage = page + 2

    if maxPage > totalPage:
        maxPage = totalPage
        minPage = totalPage - 4
        if minPage < 1:
            minPage = 1

    ret['min_page'] = int(minPage)
    ret['max_page'] = int(maxPage)
    ret['total_page'] = int(totalPage)
    ret['page'] = page

    ret['pre_page'] = True
    if page <= minPage:
        ret['pre_page'] = False

    ret['next_page'] = True
    if page >= maxPage:
        ret['next_page'] = False

    return render_template('/admin/urls.html', tplData=ret, date=(arrow.now().format('YYYYMMDD')))


#PV统计
@admin.route('/statpv/link_id/<int:linkID>/date/<date>', methods=['GET'])
@isLogin
def adminStatPV(linkID, date):
    model = AdminModel(current_app.config['DATABASE_URI'])
    linkInfo = model.getLinkInfoByID(linkID)
    if linkInfo['user_id'] != session['uid']:
        return redirect('/error?msg=' + urllib.quote('非法操作'))

    rets = {'link_id':linkID, 'list':[]}
    #rets['list'] = model.statPV(linkID, date)
    rets['date'] = date
    rets['date1'] = str(arrow.now().format('YYYYMMDD'))
    rets['date7'] = str(arrow.now().shift(days=-1).format('YYYYMMDD'))
    rets['date30'] = str(arrow.now().shift(days=-30).format('YYYYMMDD'))
    rets['urls'] = model.getUrlsByUserID(session['uid'], 0, 10)['list']
    rets['link_info'] = linkInfo

    times = []
    pvs = []
    uvs = []
    ips = []
    for info in model.statPV(linkID, date):
        if date == rets['date1']:
            times.append(str(info['time']))
        else:
            times.append(str(info['date']))
        pvs.append(int(info['pv']))
        uvs.append(int(info['uv']))
        ips.append(int(info['ip']))

    return render_template('/admin/stat_pv.html', tplData=rets, times=times, pvs=pvs, uvs=uvs, ips=ips)


#平台统计
@admin.route('/statplatform/link_id/<int:linkID>/date/<date>', methods=['GET'])
@isLogin
def adminStatPlatform(linkID, date):
    model = AdminModel(current_app.config['DATABASE_URI'])
    linkInfo = model.getLinkInfoByID(linkID)
    if linkInfo['user_id'] != session['uid']:
        return redirect('/error?msg=' + urllib.quote('非法操作'))

    rets = {'link_id':linkID, 'link_info':linkInfo, 'list':[]}
    #rets['list'] = model.statPlatform(linkID, date)
    rets['date'] = date
    rets['date1'] = str(arrow.now().format('YYYYMMDD'))
    rets['date7'] = str(arrow.now().shift(days=-1).format('YYYYMMDD'))
    rets['date30'] = str(arrow.now().shift(days=-30).format('YYYYMMDD'))
    rets['urls'] = model.getUrlsByUserID(session['uid'], 0, 10)['list']

    charts = {'legend_data':[], 'series_data':[]}
    for info in model.statPlatform(linkID, date):
        charts['legend_data'].append(info['platform'] + ': ' + str(info['total']))

        t = {}
        t['name'] = info['platform'] + ': ' + str(info['total'])
        t['value'] = info['total']
        charts['series_data'].append(t)
        del t

    return render_template('/admin/stat_platform.html', tplData=rets, charts=charts)


#环境统计
@admin.route('/statbrowser/link_id/<int:linkID>/date/<date>', methods=['GET'])
@isLogin
def adminStatBrowser(linkID, date):
    model = AdminModel(current_app.config['DATABASE_URI'])
    linkInfo = model.getLinkInfoByID(linkID)
    if linkInfo['user_id'] != session['uid']:
        return redirect('/error?msg=' + urllib.quote('非法操作'))

    rets = {'link_id':linkID, 'link_info':linkInfo, 'list':[]}
    #rets['list'] = model.statBrowser(linkID, date)
    rets['date'] = date
    rets['date1'] = str(arrow.now().format('YYYYMMDD'))
    rets['date7'] = str(arrow.now().shift(days=-1).format('YYYYMMDD'))
    rets['date30'] = str(arrow.now().shift(days=-30).format('YYYYMMDD'))
    rets['urls'] = model.getUrlsByUserID(session['uid'], 0, 10)['list']

    charts = {'legend_data':[], 'series_data':[]}
    for info in model.statBrowser(linkID, date):
        charts['legend_data'].append(info['browser'] + ': ' + str(info['total']))

        t = {}
        t['name'] = info['browser'] + ': ' + str(info['total'])
        t['value'] = info['total']
        charts['series_data'].append(t)
        del t

    return render_template('/admin/stat_browser.html', tplData=rets, charts=charts)

#环境统计
@admin.route('/stataddr/link_id/<int:linkID>/date/<date>', methods=['GET'])
@isLogin
def adminStatAddr(linkID, date):
    model = AdminModel(current_app.config['DATABASE_URI'])
    linkInfo = model.getLinkInfoByID(linkID)
    if linkInfo['user_id'] != session['uid']:
        return redirect('/error?msg=' + urllib.quote('非法操作'))

    rets = {'link_id':linkID, 'link_info':linkInfo, 'list':[]}
    #rets['list'] = model.statAddr(linkID, date)
    rets['date'] = date
    rets['date1'] = str(arrow.now().format('YYYYMMDD'))
    rets['date7'] = str(arrow.now().shift(days=-1).format('YYYYMMDD'))
    rets['date30'] = str(arrow.now().shift(days=-30).format('YYYYMMDD'))
    rets['urls'] = model.getUrlsByUserID(session['uid'], 0, 10)['list']

    charts = {'legend_data':[], 'series_data':[]}
    for info in model.statAddr(linkID, date):
        charts['legend_data'].append(info['address'] + ': ' + str(info['total']))

        t = {}
        t['name'] = info['address'] + ': ' + str(info['total'])
        t['value'] = info['total']
        charts['series_data'].append(t)
        del t

    return render_template('/admin/stat_addr.html', tplData=rets, charts=charts)


#历史记录
@admin.route('/statviewhistory/link_id/<int:linkID>/date/<date>/page/<int:page>', methods=['GET'])
@isLogin
def adminStatViewHistory(linkID, date, page):
    model = AdminModel(current_app.config['DATABASE_URI'])
    linkInfo = model.getLinkInfoByID(linkID)
    if linkInfo['user_id'] != session['uid']:
        return redirect('/error?msg=' + urllib.quote('非法操作'))

    if not page:
        page = 1

    if page < 1:
        page = 1

    limit = 10
    start = (page - 1) * limit

    rets = {'link_id':linkID, 'link_info':linkInfo, 'list':[]}
    rets['list'] = model.statViewHistory(linkID, date, start, limit)
    rets['date'] = date
    rets['date1'] = str(arrow.now().format('YYYYMMDD'))
    rets['date7'] = str(arrow.now().shift(days=-1).format('YYYYMMDD'))
    rets['date30'] = str(arrow.now().shift(days=-30).format('YYYYMMDD'))
    rets['urls'] = model.getUrlsByUserID(session['uid'], 0, 10)['list']

    #以下简化模板判断
    totalPage = math.ceil(rets['list']['total'] / (limit * 1.0))

    minPage = page - 2
    if page - 2 < 1:
        minPage = 1
        maxPage = 5
    else:
        maxPage = page + 2

    if maxPage > totalPage:
        maxPage = totalPage
        minPage = totalPage - 4
        if minPage < 1:
            minPage = 1

    rets['min_page'] = int(minPage)
    rets['max_page'] = int(maxPage)
    rets['total_page'] = int(totalPage)
    rets['page'] = page

    rets['pre_page'] = True
    if page <= minPage:
        rets['pre_page'] = False

    rets['next_page'] = True
    if page >= maxPage:
        rets['next_page'] = False

    return render_template('/admin/stat_view_history.html', tplData=rets)



