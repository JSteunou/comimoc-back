# -*- coding: utf-8 -*-


"""
Flask models that contains Documents
"""

from __future__ import unicode_literals


from flask.ext.login import UserMixin
from flask.ext.mongoengine import MongoEngine



db = MongoEngine()


class User(db.Document, UserMixin):
    """
    User document for admin purpose only
    """
    login       = db.StringField(required=True, min_length=4, unique=True)
    email       = db.EmailField(required=True, min_length=6, unique=True)
    password    = db.StringField(required=True, min_length=6)
    is_admin    = db.BooleanField(default=False)
    
    
    def __unicode__(self):
        """
        Unicode representation (mandatory for flask-admin)
        """
        return self.login
        
    
    def is_active(self):
        return self.is_admin

