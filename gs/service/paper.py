# -*- coding:utf-8 -*-
import logging

from sqlalchemy import desc

from gs.common.cdb import db
from gs.conf import const
from gs.model.blog import Paper, Tag, Book
from gs.util import mymodel, mytime

logger = logging.getLogger('paper')


class PaperSvc(object):
    def get_paper(self, paper_id):
        paper = db.session.query(Paper).get(paper_id)
        return paper

    def paper_list(self, book_id, status=0):
        q = db.session.query(Paper).filter(Paper.book_id == book_id, Paper.status == status)
        paper_list = q.all()
        return paper_list

    def blog_list(self, start=0, limit=None):  # todo 博客列表需要优化
        q = db.session.query(Paper)
        count = q.count()
        if start is not None:
            q = q.offset(start)
        if limit is not None:
            q = q.limit(limit)
        blog_list = q.all()
        return count, blog_list

    def last_paper(self):
        papers = db.session.query(Paper).order_by(desc(Paper.create_time)).limit(const.DEFAULT_LIMIT).all()
        return papers

    def tag_list(self):
        tags = db.session.query(Tag).all()
        return tags

    def book_list(self, status=0):
        books = db.session.query(Book).filter(Book.status == status).all()
        return books

    def book_save(self, book):
        book_id = book.book_id
        try:
            if not book_id:
                db.session.add(book)
            else:
                book.update_time = mytime.get_now_datetime()
                t_dict = mymodel.model_todbdict(book)
                t_dict.pop('book_id')
                t_dict.pop('create_time')
                db.session.query(Book).filter(Book.book_id == book_id).update(t_dict)
            db.session.commit()
            return True
        except Exception as e:
            logger.exception(e)
            db.session.rollback()
            return False

    def paper_save(self, paper):
        paper_id = paper.paper_id
        try:
            if not paper_id:
                db.session.add(paper)
                db.session.flush()
                paper_id = paper.paper_id
            else:
                t_dict = mymodel.model_todbdict(paper)
                t_dict.pop('paper_id')
                t_dict.pop('create_time')
                db.session.query(Paper).filter(Paper.paper_id == paper_id).update(t_dict)
            db.session.commit()
            return self.get_paper(paper_id)
        except Exception as e:
            logger.exception(e)
            return False

    def book_delete(self, book_id):
        try:
            db.session.query(Book).filter(Book.book_id == book_id).update(
                {Book.status: -1, Book.update_time: mytime.get_now_datetime()})
            self.papers_delete(book_id)
            db.session.commit()
            return True
        except Exception as e:
            logger.exception(e)
            db.session.rollback()
            return False

    def paper_delete(self, paper_id):
        try:
            db.session.query(Paper).filter(Paper.paper_id == paper_id).update(
                {Paper.status: -1, Paper.update_time: mytime.get_now_datetime()})
            db.session.commit()
            return True
        except Exception as e:
            logger.exception(e)
            db.session.rollback()
            return False

    def papers_delete(self, book_id):
        try:
            db.session.query(Paper).filter(Paper.book_id == book_id).update(
                {Paper.status: -1, Paper.update_time: mytime.get_now_datetime()})
            db.session.commit()
            return True
        except Exception as e:
            logger.exception(e)
            db.session.rollback()
            return False
