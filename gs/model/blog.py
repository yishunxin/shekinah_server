# -*- coding:utf-8 -*-
from sqlalchemy.dialects.mysql import LONGTEXT

from gs.common.cdb import db
from gs.util import mytime


class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    user_name = db.Column(db.String(255))
    password = db.Column(db.String(255))
    phone = db.Column(db.String(255))
    create_time = db.Column(db.DateTime, default=mytime.get_now_datetime)
    avatar = db.Column(db.String(255))

    def __repr__(self):
        return '<User user_id=%s>' % self.user_id


class Catalog(db.Model):
    __tablename__ = 'catalog'
    catalog_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    level = db.Column(db.Integer)
    pcatalog_id = db.Column(db.Integer)

    def __repr__(self):
        return '<Catalog catalog_id=%s>' % self.catalog_id


class Paper(db.Model):
    __tablename__ = 'paper'
    paper_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    create_time = db.Column(db.DateTime, default=mytime.get_now_datetime)
    content = db.Column(LONGTEXT)
    author = db.Column(db.String(255))
    catalog_id = db.Column(db.Integer)
    status = db.Column(db.Integer, default=0)
    book_id = db.Column(db.Integer)
    update_time = db.Column(db.DateTime)

    def __repr__(self):
        return '<Paper paper_id=%s>' % self.paper_id


class Book(db.Model):
    __tablename__ = 'book'
    book_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.String(255))
    status = db.Column(db.Integer, default=0)
    create_time = db.Column(db.DateTime, default=mytime.get_now_datetime)
    update_time = db.Column(db.DateTime)


class Essay(db.Model):
    __tablename__ = 'essay'
    essay_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    create_time = db.Column(db.DateTime, default=mytime.get_now_datetime)
    content = db.Column(LONGTEXT)
    author = db.Column(db.String(255))
    catalog_id = db.Column(db.Integer)
    status = db.Column(db.Integer)

    def __repr__(self):
        return '<Essay essay_id=%s>' % self.essay_id


class Papertag(db.Model):
    __tablename__ = 'paper_tag'
    paper_id = db.Column(db.Integer, primary_key=True)
    tag_id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return '<Papertag paper_id=%s,tag_id=%s>' % (self.paper_id, self.tag_id)


class Tag(db.Model):
    __tablename__ = 'tag'
    tag_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    def __repr__(self):
        return '<Tag tag_id=%s>' % self.tag_id
