# -*- coding: utf-8 -*-
# @Author: smallevil
# @Date:   2020-11-23 21:12:56
# @Last Modified by:   smallevil
# @Last Modified time: 2020-11-24 02:09:59

import sys,os
PY2 = True if sys.version_info.major == 2 else False
if PY2:
    reload(sys)
    sys.setdefaultencoding('UTF8')
    import ConfigParser
else:
    import configparser

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/libs')

import logging
import logging.handlers
logger = logging.getLogger()
logger.setLevel('DEBUG') # 也可以不设置，不设置就默认用logger的level
BASIC_FORMAT = "%(asctime)s:%(name)s:%(levelname)s:%(lineno)s:%(message)s"
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter(BASIC_FORMAT, DATE_FORMAT)
fhlr = logging.handlers.TimedRotatingFileHandler(os.path.realpath(os.path.split(os.path.realpath(__file__))[0] + '/logs/access.log'), when='midnight',interval=1,backupCount=5) # 输出到文件的handler
fhlr.setFormatter(formatter)
logger.addHandler(fhlr)
'''
chlr = logging.StreamHandler() # 输出到控制台的handler
chlr.setFormatter(formatter)
logger.addHandler(chlr)
'''

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
logging.getLogger('apscheduler').setLevel(logging.ERROR)


from flask import Flask
app = Flask(__name__, template_folder='tpl')
app.secret_key = b'(nm6T#cu%IUNVH?A&oZp'
from adminRoute import adminRoute
app.register_blueprint(adminRoute)


if __name__ == '__main__':

    if PY2:
        iniConf = ConfigParser.ConfigParser()
    else:
        iniConf = configparser.ConfigParser()

    iniConf.read(os.path.dirname(os.path.realpath(__file__)) + '/conf.ini')
    #print(iniConf.get('redis', 'host'))

    '''
    scheduler = BlockingScheduler()
    scheduler.add_job(job_function, 'interval', hours=1, id='sync_redis_to_db')
    scheduler.start()
    '''

    app.run(host='127.0.0.1', port=8888, debug=True)