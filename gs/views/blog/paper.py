# -*- coding:utf-8 -*-
import logging
from flask import render_template, request

from gs.common import cstore, cbusi
from gs.common.cresponse import common_json_response, jsonify_response
from gs.conf import apicode
from gs.model.blog import Book, Paper, Album, Photo, File, Essay
from gs.service.paper import PaperSvc
from gs.util import mymodel, myreq
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


@bp_blog.route('/paper/write', methods=['GET'])
def paper_write():
    try:
        book_list = PaperSvc().book_list()
        return render_template('write/write.html', book_list=book_list)
    except Exception as e:
        logger.exception(e)
        return render_template('404.html')


@bp_blog.route('/book/list', methods=['GET'])
def book_list():
    try:
        book_list = PaperSvc().book_list()
        return common_json_response(book_list=book_list)
    except Exception as e:
        logger.exception(e)
        return jsonify_response(apicode.ERROR)


@bp_blog.route('/book/save', methods=['POST'])
def book_save():
    try:
        book = mymodel.formtomodel(request.form, Book)
        bo = PaperSvc().book_save(book)
        if bo:
            return jsonify_response(apicode.OK)
        else:
            return jsonify_response(apicode.ERROR)
    except Exception as e:
        logger.exception(e)
        return jsonify_response(apicode.ERROR)


@bp_blog.route('/paper/list', methods=["GET"])
def paper_list():
    try:
        book_id = myreq.getvalue_from_request('book_id')
        paper_list = PaperSvc().paper_list(book_id)
        return common_json_response(paper_list=paper_list)
    except Exception as e:
        logger.exception(e)
        return jsonify_response(apicode.ERROR)


@bp_blog.route('/paper/save', methods=['POST'])
def paper_save():
    try:
        paper = mymodel.formtomodel(request.form, Paper)
        paper = PaperSvc().paper_save(paper)
        if paper:
            return common_json_response(paper=paper)
        else:
            return jsonify_response(apicode.ERROR)
    except Exception as e:
        logger.exception(e)
        return jsonify_response(apicode.ERROR)


@bp_blog.route('/book/delete', methods=['GET'])
def book_delete():
    try:
        book_id = myreq.getvalue_from_request('book_id')
        bo = PaperSvc().book_delete(book_id)
        if not bo:
            return jsonify_response(apicode.ERROR)
        return jsonify_response(apicode.OK)
    except Exception as e:
        logger.exception(e)
        return jsonify_response(apicode.ERROR)


@bp_blog.route('/paper/delete', methods=['GET'])
def paper_delete():
    try:
        paper_id = myreq.getvalue_from_request('paper_id')
        bo = PaperSvc().paper_delete(paper_id)
        if not bo:
            return jsonify_response(apicode.ERROR)
        return jsonify_response(apicode.OK)
    except Exception as e:
        logger.exception(e)
        return jsonify_response(apicode.ERROR)


@bp_blog.route('/upload/token', methods=['GET'])
def upload_token():
    try:
        return common_json_response(upload_token=cstore.get_token())
    except Exception as e:
        logger.exception(e)
        return jsonify_response(apicode.ERROR)


@bp_blog.route('/config/get', methods=['GET'])
def config_get():
    try:
        return common_json_response(configs=cbusi.get_configs())
    except Exception as e:
        logger.exception(e)
        return jsonify_response(apicode.ERROR)


@bp_blog.route('/album/list', methods=['GET'])
def album_list():
    try:
        albums = PaperSvc().album_list()
        return common_json_response(albums=albums)
    except Exception as e:
        logger.exception(e)
        return jsonify_response(apicode.ERROR)


@bp_blog.route('/photo/list', methods=['GET'])
def photo_list():
    try:
        aid = myreq.getvalue_from_request('aid')
        photos = PaperSvc().photo_list(aid)
        return common_json_response(photos=photos)
    except Exception as e:
        logger.exception(e)
        return jsonify_response(apicode.ERROR)


@bp_blog.route('/album/save', methods=['POST'])
def album_save():
    try:
        album = mymodel.formtomodel(request.form, Album)
        bo = PaperSvc().album_save(album)
        if not bo:
            return jsonify_response(apicode.ERROR)
        return jsonify_response(apicode.ERROR)
    except Exception as e:
        logger.exception(e)
        return jsonify_response(apicode.ERROR)


@bp_blog.route('/photo/delete', methods=['GET'])
def photo_delete():
    try:
        pids = myreq.getvalue_from_request('pids').split(',')
        opreate_type = myreq.getvalue_from_request('opreate_type')
        if opreate_type == 'delete':
            bo = PaperSvc().photo_delete(pids)
        elif opreate_type == 'recycle':
            bo = PaperSvc().photo_recycle(pids)
        if not bo:
            return jsonify_response(apicode.ERROR)
        return jsonify_response(apicode.OK)
    except Exception as e:
        logger.exception(e)
        return jsonify_response(apicode.ERROR)


@bp_blog.route('/album/delete', methods=['GET'])
def album_delete():
    try:
        aid = myreq.getvalue_from_request('aid')
        opreate_type = myreq.getvalue_from_request('opreate_type')
        if opreate_type == 'delete':
            bo = PaperSvc().album_delete(aid)
        elif opreate_type == 'recycle':
            bo = PaperSvc().album_recycle(aid)
        if not bo:
            return jsonify_response(apicode.ERROR)
        return jsonify_response(apicode.OK)
    except Exception as e:
        logger.exception(e)
        return jsonify_response(apicode.ERROR)


@bp_blog.route('/photo/save', methods=['POST'])
def photo_save():
    try:
        data = request.form
        photo = mymodel.formtomodel(data, Photo)
        key = data['path']
        file = File()
        file.path = key
        file.type = 'photo'
        file.name = photo.name
        fid = PaperSvc().file_save(file)
        if not fid:
            return jsonify_response(apicode.ERROR)
        photo.fid = fid
        bo = PaperSvc().photo_save(photo)
        if not bo:
            return jsonify_response(apicode.ERROR)
        return jsonify_response(apicode.OK)
    except Exception as e:
        logger.exception(e)
        return jsonify_response(apicode.ERROR)


@bp_blog.route('/essay/list', methods=['GET'])
def essay_list():
    try:
        essay_list = PaperSvc().essay_list()
        return common_json_response(essay_list=essay_list)
    except Exception as e:
        logger.exception(e)
        return jsonify_response(apicode.ERROR)


@bp_blog.route('/essay/save', methods=['POST'])
def essay_save():
    try:
        essay = mymodel.formtomodel(request.form, Essay)
        bo = PaperSvc().essay_save(essay)
        if not bo:
            return jsonify_response(apicode.ERROR)
        return jsonify_response(apicode.OK)
    except Exception as e:
        logger.exception(e)
        return jsonify_response(apicode.ERROR)


@bp_blog.route('/essay/delete', methods=['GET'])
def essay_delete():
    try:
        eid = myreq.getvalue_from_request('eid')
        bo = PaperSvc().essay_delete(eid)
        if not bo:
            return jsonify_response(apicode.ERROR)
        return jsonify_response(apicode.OK)
    except Exception as e:
        logger.exception(e)
        return jsonify_response(apicode.ERROR)
