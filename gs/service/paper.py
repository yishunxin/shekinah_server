# -*- coding:utf-8 -*-
import logging
from gs.common.cdb import db
from gs.conf import const
from gs.model.blog import Paper

logging.getLogger('paper')


class PaperSvc(object):
    def get_paper(self, paper_id):
        paper = db.session.query(Paper).get(paper_id)
        return paper

    def paper_list(self, start=0, limit=const.DEFAULT_LIMIT):
        q = db.session.query(Paper)
        q = q.offset(start).limit(limit)
        return q.all()
