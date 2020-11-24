# -*- coding: utf-8 -*-
# @Author: smallevil
# @Date:   2020-11-24 10:48:40
# @Last Modified by:   smallevil
# @Last Modified time: 2020-11-24 11:53:44

from flask import Blueprint, render_template, redirect, session, request, current_app
import functools

admin = Blueprint('admin', __name__, url_prefix='/admin')

def isLogin(func):
    @functools.wraps(func) # 修饰内层函数，防止当前装饰器去修改被装饰函数的属性
    def inner(*args, **kwargs):
        # 从session获取用户信息，如果有，则用户已登录，否则没有登录
        uid = session.get('uid')
        un = session.get('un')
        level = session.get('level')
        if not user_id or not un or not level:
            return redirect('/login') #没有登录就跳转到登录路由下
        else:
            # 已经登录的话 g变量保存用户信息，相当于flask程序的全局变量
            g.user_id = user_id
            return func(*args, **kwargs)
    return inner


#后台登录
@admin.route('/login', methods=['GET'])
def adminLogin():
    session.clear
    print(current_app.config)
    return render_template('/admin/login.html')


#后台首页
@admin.route('/', methods=['GET', 'POST'])
def adminIndex():
    if request.method == 'POST':
        nick = request.form.get('nick')
        passwd = request.form.get('passwd')
        return redirect('/admin/main')

    return redirect('/admin/login')


#后台退出页
@admin.route('/logout', methods=['GET', 'POST'])
@isLogin
def adminLogout():
    session.clear
    return redirect('/admin/')


#后台欢迎页
@admin.route('/main', methods=['GET'])
@isLogin
def adminMain():
    return render_template('/admin/main.html')