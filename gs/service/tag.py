# -*- coding:utf-8 -*-
import logging

from gs.common.cdb import db
from gs.model.blog import Tag

logging.getLogger('tag')


class TagSvc(object):
    def tag_list(self):
        q = db.session.query(Tag).all()
        return q
