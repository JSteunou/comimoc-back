# -*- coding: utf-8 -*-


"""
Flask models that contains Documents
"""

from __future__ import unicode_literals


from flask.ext.mongoengine import MongoEngine

import datetime
import hashlib
import copy



db = MongoEngine()


class Comment(db.Document):
    """
    A Comment is just a single comment on a page for a website
    """
    website         = db.StringField(required=True)
    page            = db.StringField(required=True)
    content         = db.StringField(required=True)
    when            = db.DateTimeField(default=datetime.datetime.utcnow)
    author_name     = db.StringField(required=True)
    author_email    = db.StringField(required=True)
    author_website  = db.StringField()
    
    def __unicode__(self):
        """
        Unicode representation (mandatory for flask-admin)
        """
        return self.content[:25]
    
    
    def to_dict(self):
        """
        Convert Document object into proper dict
        easy to convert in json (no ObjectId) and
        with email converted so it does not get public
        """
        data = copy.deepcopy(self._data)
        data['author_email'] = hashlib.md5(data['author_email']).hexdigest()
        # convert object id
        data['id'] = unicode(data['id'])
        
        return data
