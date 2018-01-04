# -*- coding:utf-8 -*-

from flask import Blueprint

from gs.conf import server

bp_blog = Blueprint('blog', __name__,
                    template_folder='templates',
                    static_folder='static')
import blog
