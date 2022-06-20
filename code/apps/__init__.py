# -*- coding: utf-8 -*-
# @Author: smallevil
# @Date:   2020-11-24 10:48:40
# @Last Modified by:   smallevil
# @Last Modified time: 2020-12-04 18:33:34

from flask import Flask
from werkzeug.contrib.fixers import ProxyFix
from .views.share import share
from .views.admin import admin
from .views.front import front
from .models.AdminModel import AdminModel
import os, logging, logging.handlers

app = Flask(__name__, template_folder='templates', static_folder='static', instance_relative_config=True)
#app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)  #修复https会跳到http的问题
app.config.from_object('config')
app.config.from_pyfile('config.py')
app.register_blueprint(share)
app.register_blueprint(admin)
app.register_blueprint(front)


logger = logging.getLogger()
BASIC_FORMAT = "%(asctime)s:%(name)s:%(levelname)s:%(lineno)s:%(message)s"
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter(BASIC_FORMAT, DATE_FORMAT)
fhlr = logging.handlers.TimedRotatingFileHandler(os.path.realpath(os.path.split(os.path.realpath(__file__))[0] + '/data/logs/access.log'), when='midnight',interval=1,backupCount=1) # 输出到文件的handler
fhlr.setFormatter(formatter)
logger.addHandler(fhlr)

if app.config['DEBUG']:
    logger.setLevel(logging.DEBUG) # 也可以不设置，不设置就默认用logger的level
    chlr = logging.StreamHandler() # 输出到控制台的handler
    chlr.setFormatter(formatter)
    logger.addHandler(chlr)
else:
    logger.setLevel(logging.INFO)
