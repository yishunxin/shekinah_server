# -*- coding:utf-8 -*-
from flask import render_template

from gs.views import bp_blog


@bp_blog.route('/index')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        print e
        return render_template('404.html')
