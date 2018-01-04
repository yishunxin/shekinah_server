# -*- coding:utf-8 -*-
from flask import jsonify

from gs.common import recurjson


def jsonify_response(code, msg=None, data=None, **kwdata):
    return jsonify(code=code, msg=msg, data=data, **kwdata)


def common_json_response(**kwdata):
    return recurjson.encode(kwdata)


def common_json_entity(entity):
    return recurjson.encode(entity)


def common_json_entities(*args):
    return recurjson.encode(args)
