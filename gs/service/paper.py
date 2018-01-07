# -*- coding:utf-8 -*-
import logging

from sqlalchemy import desc

from gs.common.cdb import db
from gs.conf import const
from gs.model.blog import Paper

logging.getLogger('paper')


class PaperSvc(object):
    def get_paper(self, paper_id):
        paper = db.session.query(Paper).get(paper_id)
        return paper

    def paper_list(self, start=None, limit=const.DEFAULT_LIMIT):
        q = db.session.query(Paper)
        count = q.count()
        if start is not None:
            q = q.offset(start).limit(limit)
        paper_list = q.all()
        return count, paper_list

    def last_paper(self):
        papers = db.session.query(Paper).order_by(desc(Paper.create_time)).limit(const.DEFAULT_LIMIT).all()
        return papers
