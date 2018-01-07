# -*- coding:utf-8 -*-
import logging
from flask import render_template

from gs.common.pager import Pager
from gs.conf import const
from gs.service.paper import PaperSvc
from gs.util import myreq
from gs.views import bp_blog

logger = logging.getLogger('index')


@bp_blog.route('/')
def index():
    try:
        curr_page = myreq.getvalue_from_request('curr_page', 1)
        limit = const.DEFAULT_LIMIT
        start = (curr_page - 1) * limit
        count, paper_list = PaperSvc().paper_list(start=start, limit=limit)
        pager = Pager()
        pager.page = curr_page
        pager.total = (count + limit - 1) / limit
        pager.size = limit
        pager.set_nums(pager.def_show_page_num)
        return render_template('index.html', total_num=count, paper_list=paper_list,pager=pager)
    except Exception as e:
        print e
        return render_template('404.html')
