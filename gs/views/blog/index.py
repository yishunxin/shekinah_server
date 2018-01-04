# -*- coding:utf-8 -*-
import logging
from flask import render_template

from gs.conf import const
from gs.service.paper import PaperSvc
from gs.util import myreq
from gs.views import bp_blog

logger = logging.getLogger('index')


@bp_blog.route('/index')
def index():
    try:
        curr_page = myreq.getvalue_from_request('curr_page', 1)
        limit = const.DEFAULT_LIMIT
        start = (curr_page - 1) * limit
        paper_list = PaperSvc().paper_list(start=start, limit=limit)
        return render_template('index.html')
    except Exception as e:
        print e
        return render_template('404.html')


@bp_blog.route('/')
def base():
    try:
        return render_template('base.html')
    except Exception as e:
        logger.exception(e)
        return render_template('404.html')
