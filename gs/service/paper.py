# -*- coding:utf-8 -*-
import datetime
import logging

from sqlalchemy import desc

from gs.common.cdb import db
from gs.conf import const, store
from gs.model.blog import Paper, Tag, Book, Album, Photo, File, Essay, Note
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
        q = db.session.query(Paper).filter(Paper.status == 0)
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

    def album_list(self):
        return db.session.query(Album).filter(Album.status == 0).order_by(desc(Album.create_time)).all()

    def photo_list(self, aid):
        q = db.session.query(Photo, File.path).filter(Photo.fid == File.fid, Photo.album_id == aid,
                                                      Photo.status == 0).order_by(
            desc(Photo.create_time)).all()
        result = list()
        for photo, path in q:
            photo.file = store.domain + '/' + path
            result.append(photo)
        return result

    def album_save(self, album):
        aid = album.aid
        try:
            if not aid:
                db.session.add(album)
            else:
                t_dict = mymodel.model_todbdict(album)
                t_dict.pop('aid')
                t_dict.pop('create_time')
                db.session.query(Album).filter(Album.aid == aid).update(t_dict)
            db.session.commit()
            return True
        except Exception as e:
            logger.exception(e)
            db.session.rollback()
            return False

    def photo_save(self, photo):
        pid = photo.pid
        try:
            if not pid:
                db.session.add(photo)
            else:
                t_dict = mymodel.model_todbdict(photo)
                t_dict.pop('pid')
                t_dict.pop('fid')
                t_dict.pop('album_id')
                db.session.query(Photo).filter(Photo.pid == pid).update(t_dict)
            db.session.commit()
            return True
        except Exception as e:
            logger.exception(e)
            db.session.rollback()
            return False

    def album_get(self, aid):
        return db.session.query(Album).get(aid)

    def album_delete(self, aid):
        try:
            album = self.album_get(aid)
            photos = db.session.query(Photo).filter(Photo.album_id == aid).all()
            fids = [photo.fid for photo in photos]
            if album.cover:
                fids.append(album.cover)
            db.session.query(Album).filter(Album.aid == aid).delete()
            db.session.query(Photo).filter(Photo.album_id == aid).delete()
            db.session.query(File).filter(File.fid.in_(fids)).delete(synchronize_session='fetch')
            db.session.commit()
            return True
        except Exception as e:
            logger.exception(e)
            db.session.rollback()
            return False

    def photo_delete(self, pids):
        try:
            db.session.query(File).filter(File.fid == Photo.fid, Photo.pid.in_(pids)).delete(
                synchronize_session='fetch')
            db.session.query(Photo).filter(Photo.pid.in_(pids)).delete(synchronize_session='fetch')
            db.session.commit()
            return True
        except Exception as e:
            logger.exception(e)
            return False

    def file_save(self, file):
        try:
            db.session.add(file)
            db.session.flush()
            db.session.commit()
            return file.fid
        except Exception as e:
            logger.exception(e)
            return False

    def photo_recycle(self, pids):
        try:
            db.session.query(Photo).filter(Photo.pid.in_(pids)).update(Photo.status == -1, synchronize_session='fetch')
            db.session.commit()
            return True
        except Exception as e:
            logger.exception(e)
            return False

    def album_recycle(self, aid):
        try:
            db.session.query(Photo).filter(Photo.album_id == aid).update(Photo.status == -1)
            db.session.query(Album).filter(Album.aid == aid).delete()
            db.session.commit()
            return True
        except Exception as e:
            logger.exception(e)
            return False

    def essay_list(self):
        essay_list = db.session.query(Essay).order_by(desc(Essay.create_time)).all()
        for essay in essay_list:
            essay.photo_list = essay.photos.split(',') if essay.photos else []
            essay.video_list = essay.videos.split(',') if essay.videos else []
        return essay_list

    def essay_save(self, essay):
        try:
            db.session.add(essay)
            db.session.commit()
            return True
        except Exception as e:
            logger.exception(e)
            db.session.rollback()
            return False

    def essay_delete(self, eid):
        try:
            db.session.query(Essay).filter(Essay.eid == eid).delete()
            db.session.commit()
            return True
        except Exception as e:
            logger.exception(e)
            db.session.rollback()
            return False

    def note_save(self, note):
        try:
            db.session.add(note)
            db.session.commit()
            return True
        except Exception as e:
            logger.exception(e)
            db.session.rollback()
            return False

    def note_list(self, year, month):
        month_begin = mytime.get_lastday_of_month(year, month)
        month_end = datetime.datetime(year, month, 01, 0, 0, 0)
        notes = db.session.query(Note).filter(Note.status != -1, Note.create_time >= month_begin,
                                              Note.create_time <= month_end).order_by(Note.create_time).all()
        for note in notes:
            note.status_bo = True if note.status == 2 else False
        return notes

    def note_changestatus(self, nid, status):
        try:
            db.session.query(Note).filter(Note.nid == nid).update(Note.status == status)
            db.session.commit()
            return True
        except Exception as e:
            logger.exception(e)
            db.session.rollback()
            return False
