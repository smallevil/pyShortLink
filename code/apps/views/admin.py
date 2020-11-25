# -*- coding: utf-8 -*-
# @Author: smallevil
# @Date:   2020-11-24 10:48:40
# @Last Modified by:   smallevil
# @Last Modified time: 2020-11-25 13:28:08

from flask import Blueprint, render_template, redirect, session, request, current_app
import functools
from ..models.AdminModel import AdminModel

import math

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


#添加短链
@admin.route('/add', methods=['GET', 'POST'])
@isLogin
def adminAdd():
    if request.method == 'POST':
        url = request.form.get('url')
        domain = request.form.get('domain')
        if url and domain:
            model = AdminModel(current_app.config['DATABASE_URI'])
            ret = model.addLinkInfo(session.get('uid'), url, domain)
            if ret:
                return redirect('/admin/stat/' + ret['key'])

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

    return render_template('/admin/urls.html', tplData=ret)












