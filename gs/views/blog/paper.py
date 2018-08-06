# -*- coding:utf-8 -*-
import logging
from flask import render_template, request

from gs.common.cresponse import common_json_response, jsonify_response
from gs.conf import apicode
from gs.model.blog import Book, Paper
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
