# -*- coding: utf-8 -*-
# @Author: smallevil
# @Date:   2020-11-24 10:48:40
# @Last Modified by:   smallevil
# @Last Modified time: 2020-11-26 01:40:33

from apps import app
from flask_apscheduler import APScheduler
import arrow
from apps.models.AdminModel import AdminModel

def statDay():
    model = AdminModel(app.config['DATABASE_URI'])
    model.setStatDay()

if __name__ == '__main__':
    scheduler = APScheduler()
    #scheduler.add_job(func=statDay, id='stat_day', trigger='interval', minutes=5)
    scheduler.add_job(func=statDay, id='stat_day', trigger='cron', minute='0,5,10,15,20,25,30,35,40,45,50,55')
    scheduler.start()

    app.run(host='0.0.0.0', port=8888)