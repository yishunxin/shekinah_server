# -*- coding:utf-8 -*-
import logging
from flask import render_template

from gs.views import bp_blog

logging.getLogger('index')


@bp_blog.route('/index')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        print e
        return render_template('404.html')
