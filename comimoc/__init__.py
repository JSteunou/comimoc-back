#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Comimoc is light backend that provide a RESTful API to handle comments
    and a UI for easy administration.
    It uses MongoDB to store data and it handle CORS.

    It is built with Flask and Flask-MongoEngine but also Flask-Admin, Flask-Login,
    and Flask-WTF

    Flask documentation: http://flask.pocoo.org/docs/
    Flask-MongoEngine documentation: https://flask-mongoengine.readthedocs.org/
    Flask-Admin documentation: https://flask-admin.readthedocs.org/
    Flask-Login documentation: https://flask-login.readthedocs.org/

    This file creates the application through `create_app` and return it.
    Use it to call run() directly or give it do WSGI capable server.
"""

# OS WSGI do not like unicode in headers
# from __future__ import unicode_literals


from comimoc import settings
from comimoc.admin.views import LoginView
from comimoc.admin.views import CommentModelView
from comimoc.admin.views import UserModelView
from comimoc.admin.models import User
from comimoc.models import db
from comimoc.views import comments_bp


from flask import Flask
from flask import request
from flask.ext.admin import Admin
from flask.ext.login import LoginManager



__version__ = '0.9.3'


__all__ = ['create_app']


def create_app(options):
    """
        Create the application. Files outside the app directory can import
        this function and use it to create the application
    """
    app = Flask(__name__)
    
    # config
    app.config.from_object(settings)
    app.config.update(options)
    
    # views as blueprint
    app.register_blueprint(comments_bp)
    
    # db
    db.init_app(app)
    
    # admin
    admin = Admin(app, name="Comimoc", index_view=LoginView(app.config, name="Index"))
    admin.add_view(CommentModelView())
    admin.add_view(UserModelView())
    
    # login
    login_manager = LoginManager(app)
    @login_manager.user_loader
    def load_user(user_id):
        # .first() return None if no user as Flask-Login needs
        return User.objects(id=user_id).first()
    
    # CORS
    @app.after_request
    def add_headers(response):
        '''
        Add some headers to the response
        to be able to perform some CORS request
        '''
        if not app.config.get("USE_CORS", False):
            return response
        
        origin = request.headers.get("Origin")
        if origin not in app.config['CORS_ALLOW_ORIGIN_WHITELIST']:
            return response
        
        response.headers.add('Access-Control-Allow-Origin', origin)
        if app.config['CORS_ALLOW_CREDENTIALS']:
            response.headers.add('Access-Control-Allow-Credentials', 'true')
        response.headers.add('Access-Control-Allow-Methods', app.config['CORS_ALLOW_METHODS'])
        response.headers.add('Access-Control-Allow-Headers', app.config['CORS_ALLOW_HEADERS'])
        response.headers.add('Access-Control-Max-Age', app.config['CORS_MAX_AGE'])
        
        return response
    
    # ping pong
    @app.route('/ping', methods=['GET'])
    def ping():
        return 'pong', 200
    
    
    return app
