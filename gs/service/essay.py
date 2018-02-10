# -*- coding:utf-8 -*-
import logging

from sqlalchemy import desc

from gs.common.cdb import db
from gs.conf import const
from gs.model.blog import Paper, Tag, Essay

logging.getLogger('essay')


class EssaySvc(object):
    def get_paper(self, essay_id):
        essay = db.session.query(Essay).get(essay_id)
        return essay

    def essay_list(self, start=None, limit=const.DEFAULT_LIMIT):
        q = db.session.query(Essay)
        count = q.count()
        if start is not None:
            q = q.offset(start).limit(limit)
        essay_list = q.all()
        return count, essay_list

    def last_essay(self):
        papers = db.session.query(Essay).order_by(desc(Essay.create_time)).limit(const.DEFAULT_LIMIT).all()
        return papers

    def tag_list(self):
        tags = db.session.query(Tag).all()
        return tags
