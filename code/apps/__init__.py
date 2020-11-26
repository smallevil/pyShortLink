# -*- coding: utf-8 -*-
# @Author: smallevil
# @Date:   2020-11-24 10:48:40
# @Last Modified by:   smallevil
# @Last Modified time: 2020-11-26 12:28:01

from flask import Flask
from .views.admin import admin
from .views.front import front
from .models.AdminModel import AdminModel

app = Flask(__name__, template_folder='templates', static_folder='static', instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')
app.register_blueprint(front)
app.register_blueprint(admin)
