# -*- coding: utf-8 -*-
# @Author: smallevil
# @Date:   2020-11-24 10:48:40
# @Last Modified by:   smallevil
# @Last Modified time: 2020-11-27 02:32:24


from apps import app
from flask_apscheduler import APScheduler
import arrow, argparse
from apps.models.AdminModel import AdminModel

from gevent.pywsgi import WSGIServer
from gevent import monkey


def statMinute():
    app.logger.info('start stat minute')
    model = AdminModel(app.config['DATABASE_URI'])
    model.setStatDay('minute')

def statDay():
    app.logger.info('start stat day')
    model = AdminModel(app.config['DATABASE_URI'])
    model.setStatDay('day')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='短链接服务python版')
    parser.add_argument('-i', '--ip', type=str, help='server ip', default='0.0.0.0')
    parser.add_argument('-p', '--port', type=int, help='端口', default=10000)
    args = parser.parse_args()

    scheduler = APScheduler()
    #scheduler.add_job(func=statDay, id='stat_day', trigger='interval', minutes=5)
    scheduler.add_job(func=statMinute, id='stat_minute', trigger='cron', minute='0,5,10,15,20,25,30,35,40,45,50,55')
    scheduler.add_job(func=statDay, id='stat_day', trigger='cron', hour='0', minute='0', second='0')
    scheduler.start()

    if app.config['DEBUG']:
        app.run(host=args.ip, port=args.port)
    else:
        server  = WSGIServer((args.ip, args.port), app)
    server.serve_forever()
