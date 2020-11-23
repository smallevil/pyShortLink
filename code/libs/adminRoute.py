# -*- coding: utf-8 -*-
# @Author: smallevil
# @Date:   2020-11-23 22:55:02
# @Last Modified by:   smallevil
# @Last Modified time: 2020-11-24 02:09:21

from flask import Blueprint, session, redirect, url_for, escape, request, render_template
import functools

adminRoute = Blueprint('adminRoute', __name__)

def isLogin(func):
    @functools.wraps(func) # 修饰内层函数，防止当前装饰器去修改被装饰函数的属性
    def inner(*args, **kwargs):
        # 从session获取用户信息，如果有，则用户已登录，否则没有登录
        uid = session.get('uid')
        un = session.get('un')
        level = session.get('level')
        if not user_id or not un or not level:
            return redirect('/admin/login') #没有登录就跳转到登录路由下
        else:
            # 已经登录的话 g变量保存用户信息，相当于flask程序的全局变量
            g.user_id = user_id
            return func(*args, **kwargs)
    return inner


#后台登录
@adminRoute.route('/admin/login', methods=['GET'])
def adminLogin():
    session.clear
    return render_template('/admin/login.html')


#后台首页
@adminRoute.route('/admin/', methods=['GET', 'POST'])
def adminIndex():
    if request.method == 'POST':
        nick = request.form.get('nick')
        passwd = request.form.get('passwd')
        return redirect('/admin/main')

    return redirect('/admin/login')


#后台退出页
@adminRoute.route('/logout', methods=['GET', 'POST'])
@isLogin
def adminLogout():
    session.clear
    return redirect('/admin/')


#后台欢迎页
@adminRoute.route('/main', methods=['GET'])
@isLogin
def adminMain():
    return render_template('/admin/main.html')