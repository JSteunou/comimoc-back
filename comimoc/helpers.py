# -*- coding: utf-8 -*-


"""
Flask helpers that contains conveniant functions
"""

from __future__ import unicode_literals


import flask

from functools import wraps



def inject_args(*required_args, **default_args):
    '''
    Decorator injecting query arguments present in the request
    
    :param required_args: list of mandatory fields names
    :param default_args: dict of fields names with default values
    :raise ValueError: if required args are not present
    '''
    def wrapper(f):
        
        @wraps(f)
        def wrapped_f(*args, **kwargs):
            
            # add required_args or raise ValueError
            if all(key in flask.request.args for key in required_args):
                # update kwargs with 'inputs' dict containing all key / values
                kwargs.update({key: flask.request.args[key] for key in required_args})
            else:
                given_fields = ', '.join(flask.request.args.keys())
                expected_fields = ', '.join(required_args)
                raise ValueError("Fields missing in request.args.\nExpected: {}\nFound: {}" % (expected_fields, given_fields))
            
            # add not required args with their default values
            kwargs.update({key: flask.request.args.get(key, default_args[key]) for key in default_args.keys()})
            
            return f(*args, **kwargs)
            
        return wrapped_f
        
    return wrapper
