# -*- coding: utf-8 -*-
# @Author: smallevil
# @Date:   2020-11-24 10:48:40
# @Last Modified by:   smallevil
# @Last Modified time: 2020-11-24 13:02:09

from flask import Blueprint, render_template, redirect, session, request, current_app

front = Blueprint('front', __name__)

#前台404
@front.route('/error')
def frontError():
    return render_template('/error')


#前台首页
@front.route('/<key>')
def frontIndex(key):
    print(current_app.config)
    return key


