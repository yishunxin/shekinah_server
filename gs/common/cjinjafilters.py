# -*- coding:utf-8 -*-
import json
import logging
import md5
from gs.conf.dict import MYDICT
import time
from gs.conf import server
from random import random
from flask import session
import uuid
from gs.util import mytime

logger = logging.getLogger('common')


def init(app):
    # global 
    app.jinja_env.globals.update(RANDOM=session_random)
    # filters
    app.jinja_env.filters['datetimeformat'] = datetimeformat
    app.jinja_env.filters['hexdigest'] = hexdigest
    app.jinja_env.filters['dictitemname'] = dictitemname
    app.jinja_env.filters['dictitems'] = dictitems
    app.jinja_env.filters['version'] = version
    app.jinja_env.filters['dateweek'] = dateweek
    app.jinja_env.filters['strtodate'] = strtodate


def session_random():
    if 'user' in session:
        return session['user']['userid'] + str(random())
    else:
        return str(uuid.uuid4()) + str(random())


def datetimeformat(value, format='%Y-%m-%d %H:%M:%S'):
    return value.strftime(format) if value else ''


def strtodate(value, format='%Y-%m-%d %H:%M:%S'):
    value = mytime.parse_time(value)
    return value.strftime(format)


def hexdigest(value):
    try:
        return md5.md5(value.encode('utf-8', 'ignore')).hexdigest()
    except Exception, e:
        logger.exception(e)
        return ''


def dictitemname(value, dictname):
    try:
        return MYDICT[dictname][value]
    except Exception, e:
        return ''


def dictitems(dictname):
    key = dictname + '_LIST'
    if key not in MYDICT:
        MYDICT[key] = items = []
        for k, v in MYDICT[dictname].iteritems():
            items.append({'key': k, 'value': v})
    return MYDICT[key]


def version(value):
    if server.ONLINE:
        return server.VERSION
    return int(time.time())


def dateweek(value):
    try:
        return mytime.format_week(value)
    except Exception, e:
        logger.exception(e)
        return ''
