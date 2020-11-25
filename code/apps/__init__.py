# -*- coding: utf-8 -*-
# @Author: smallevil
# @Date:   2020-11-24 10:48:40
# @Last Modified by:   smallevil
# @Last Modified time: 2020-11-24 12:54:04

from flask import Flask
from views import admin
from views import front
from models import AdminModel

app = Flask(__name__, template_folder='templates', static_folder='static', instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')
app.register_blueprint(front)
app.register_blueprint(admin)
