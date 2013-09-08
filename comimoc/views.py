# -*- coding: utf-8 -*-


"""
Flask views that contains Blueprints
"""

from __future__ import unicode_literals


from comimoc.models import Comment
from comimoc.helpers import inject_args

from flask import Blueprint
from flask import jsonify
from flask import request



comments_bp = Blueprint('comments_bp', __name__)


@comments_bp.route('/comments', methods=['GET'])
@inject_args(website="", page="")
def get_all_comments(website, page):
    coms = Comment.objects(website=website, page=page)
    return jsonify(comments=[com.to_dict() for com in coms])


@comments_bp.route('/comments', methods=['POST'])
def add_comment():
    com = Comment(**request.get_json())
    com.save()
    return jsonify(**com.to_dict()), 201
