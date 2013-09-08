# -*- coding: utf-8 -*-


"""
Default settings
"""

# do not forget to provide your own secret key
# used for CSRF protection and Session cookies
SECRET_KEY = None

# use cross origin resource sharing
USE_CORS = True
# do not use wildcard '*' or you won't be able to use credentials
CORS_ALLOW_ORIGIN_WHITELIST = ()
# allow credentials (useful for cookie)
CORS_ALLOW_CREDENTIALS = True
# RESTful CRUD + OPTIONS
CORS_ALLOW_METHODS = 'GET, POST, PUT, DELETE, OPTIONS'
# some useful headers
CORS_ALLOW_HEADERS = 'content-type, accept, origin'
# 20 days
CORS_MAX_AGE = 1728000

# By default only the first user registered is automatically an admin
# others are just registered but have no access.
# If you fear for your app security or do not want to check by hand all the users
# that should automatically be admin add here a list of admin emails.
# 
ADMIN_EMAILS = ()