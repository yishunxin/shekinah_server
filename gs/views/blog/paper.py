# -*- coding:utf-8 -*-
import logging
from flask import render_template

from gs.service.paper import PaperSvc
from gs.views import bp_blog

logger = logging.getLogger('index')


@bp_blog.route('/paper/detail/<int:paper_id>', methods=['GET'])
def paper_detail(paper_id):
    try:
        paper = PaperSvc().get_paper(paper_id)
        return render_template('detail.html', paper=paper)
    except Exception as e:
        logger.exception(e)
        return render_template('404.html')
