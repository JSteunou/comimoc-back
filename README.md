# Comimoc Back

Comimoc Back is the backend part of the Comimoc project.

It is a light backend that provide a RESTful API to handle comments and a UI for easy administration.

It uses MongoDB to store data and it is built with [Flask](http://flask.pocoo.org) + powerful extensions:

* [Flask-Admin](https://github.com/mrjoes/flask-admin/)
* [Flask-Login]()
* [Flask-MongoEngine](https://github.com/MongoEngine/flask-mongoengine)
* [Flask-WTF]()

# Features

* Store simple comments for pages for as much as website you want
* Provide a simple admin GUI on which you can handle your comments
* Support multiple administrator

# How to:

## install it

Then you just `pip install comimoc` or git clone https://github.com/JSteunou/comimoc-back

## run it

The Flask application is available through `comimoc.create_app(options)` which will return you a Flask app you could use with every WSGI capable server. So all you have to do is to give your settings and get back the app to expose it.

Example with a file mycomimoc.py

```python
from comimoc import create_app

options = {
    "SECRET_KEY": "Your secret key goes here",
    "MONGODB_SETTINGS": {
        "DB": "comimoc",
        "HOST": "http://domain.com",
        "PORT": "123456",
        "USERNAME": "admin",
        "PASSWORD": "admin",
        },
    "CORS_ALLOW_ORIGIN_WHITELIST": ('http://jeromesteunou.net', 'http://www.jeromesteunou.net')
}
flask_app = create_app(options)
```

Then you can run gunicorn:

```
$ gunicorn mycomimoc:flask_app
```

More information about [how deploying a Flask app](http://flask.pocoo.org/docs/deploying/others/)

**About the SECRET_KEY**

Do not forget to provide your own. The application just won't work without it. It needs it for CSRF and cookie protection. You can easly create one with python:

```python
>>> import os
>>> os.urandom(24)
'`\x13o\xb7N\xe8\x1ds\x04:Q\xeav\x10\xec\x06\xc7\x8fS\xe6)T1I'
```



## settings

The options must give when creating the application can contains all [Flask](http://flask.pocoo.org/docs/config/#builtin-configuration-values) and [Flask-MongoEngine settings](https://flask-mongoengine.readthedocs.org/en/latest/) plus the Comimoc settings

* **USE\_CORS**: Boolean. Use [cross origin resource sharing](https://developer.mozilla.org/en-US/docs/HTTP/Access_control_CORS) by adding HTTP Headers depending on the **CORS\_\*** settings below. This allow you to have the front-end and the back-end on different domains. Very useful for multiple front and one back-end. *default: True*.
* **CORS\_ALLOW\_ORIGIN\_WHITELIST**: List of string. List of your front-end URL if you set **USE\_CORS** on `True`. Do not forget the scheme (http://, https://). Tips: you may need to add the root domain and the www subdomain if your site is available on both. *default: ()* (empty).
* **CORS\_ALLOW\_CREDENTIALS**: Boolean. Allow credentials. Mandatory if you want the browser to send cookie in CORS with preflight requests. Comimoc does not need it for now. *default: True*.
* **CORS\_ALLOW\_METHODS**: String. Specifies the method or methods allowed when accessing the resource. It will be surprising if you have to change this one. *default: 'GET, POST, PUT, DELETE, OPTIONS'*.
* **CORS\_ALLOW\_HEADERS**: String. Used in response to a preflight request to indicate which HTTP headers can be used when making the actual request. Default value works fine with Comimoc Front, but you may adapt it to your situation especially if you are using custom HTTP headers. *default: 'content-type, accept, origin'*.
* **ADMIN\_EMAILS**: List of string. By default only the first user registered is automatically an administrator. Others are just registered but have no access. If you fear for your app security or do not want to check by hand all the users that should automatically be admin add here a list of admin emails. *default: ()* (empty).

## use it

For getting and posting comments, best is to use it with Comimoc Front which is an AngularJS application easily customisable

