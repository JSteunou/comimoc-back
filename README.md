# Comimoc Back

Comimoc Back is the back-end part of the Comimoc project.

It is a light backend that provide a RESTful API to handle comments and a UI for easy administration.

It uses MongoDB to store data and it is built with [Flask](http://flask.pocoo.org) + powerful extensions:

* [Flask-Admin](https://github.com/mrjoes/flask-admin/)
* [Flask-Login](https://github.com/maxcountryman/flask-login/)
* [Flask-MongoEngine](https://github.com/MongoEngine/flask-mongoengine/)
* [Flask-WTF](https://flask-wtf.readthedocs.org)


# Features

* Store simple comments for pages for as much as website you want
* Provide a simple admin GUI on which you can handle your comments
* Support multiple administrator


# How to:

## install it

You need MongoDB and python 2.7.
Then just `pip install comimoc` or get the source on https://github.com/JSteunou/comimoc-back

Example in a [virtual env](http://www.virtualenv.org):

```shell
$ virtualenv ~/virtualenvs/comimoc
$ cd ~/virtualenvs/comimoc
$ . bin/activate
(comimoc)$ pip install comimoc
```

## run it

The Flask application is available through `comimoc.create_app(options)` which will return you a Flask app you could use with every WSGI capable server. So all you have to do is to give it your settings and get back the app to expose it.

Example with [gunicorn](http://gunicorn.org):

Still in our virtual env, install gunicorn and create a simple application creator.

```shell
(comimoc)$ pip install gunicorn
(comimoc)$ touch mycomimoc.py
```

Paste this down in it

```python
from comimoc import create_app

options = {
    "SECRET_KEY": "Your secret key goes here",
    "MONGODB_SETTINGS": {
        "DB": "comimoc",
        },
    "CORS_ALLOW_ORIGIN_WHITELIST": ('http://yourdomain.net', 'http://www.yourdomain.net')
}
flask_app = create_app(options)
```

And run gunicorn

```shell
(comimoc)$ gunicorn mycomimoc:flask_app
2013-09-08 21:15:15 [24925] [INFO] Starting gunicorn 18.0
2013-09-08 21:15:15 [24925] [INFO] Listening at: http://127.0.0.1:8000 (24925)
2013-09-08 21:15:15 [24925] [INFO] Using worker: sync
2013-09-08 21:15:15 [24930] [INFO] Booting worker with pid: 24930
```

Et voilà, your comimoc back-end is running. Of course gunicorn can take many options and you might want to run a server in front like Apacha or Nginx. More information about [how deploying a Flask app](http://flask.pocoo.org/docs/deploying/others/)

**About the SECRET_KEY**

Do not forget to provide your own. The application just won't work without it. It needs it for CSRF and cookie protection. You can easily create one with python:

```python
>>> import os
>>> os.urandom(24)
'`\x13o\xb7N\xe8\x1ds\x04:Q\xeav\x10\xec\x06\xc7\x8fS\xe6)T1I'
```

## set it

The options you have to give when creating the application can contain all [Flask](http://flask.pocoo.org/docs/config/#builtin-configuration-values) and [Flask-MongoEngine](https://flask-mongoengine.readthedocs.org/en/latest/) settings in addition to the Comimoc settings.

* **USE\_CORS**: Boolean. Use [cross origin resource sharing](https://developer.mozilla.org/en-US/docs/HTTP/Access_control_CORS) by adding HTTP Headers depending on the **CORS\_*** settings below. This allow you to have the front-end and the back-end on different domains. Very useful for multiple front and one back-end. *default: True*.
* **CORS\_ALLOW\_ORIGIN\_WHITELIST**: List of string. List of your front-end URL if you set **USE\_CORS** on `True`. Do not forget the scheme (http://, https://). Tips: you may need to add the root domain and the www subdomain if your site is available on both. *default: ()* (empty).
* **CORS\_ALLOW\_CREDENTIALS**: Boolean. Allow credentials. Mandatory if you want the browser to send cookie in CORS with preflight requests. Comimoc does not need it for now. *default: True*.
* **CORS\_ALLOW\_METHODS**: String. Specifies the method or methods allowed when accessing the resource. It will be surprising if you have to change this one. *default: 'GET, POST, PUT, DELETE, OPTIONS'*.
* **CORS\_ALLOW\_HEADERS**: String. Used in response to a preflight request to indicate which HTTP headers can be used when making the actual request. Default value works fine with Comimoc Front, but you may adapt it to your situation especially if you are using custom HTTP headers. *default: 'content-type, accept, origin'*.
* **ADMIN\_EMAILS**: List of string. By default only the first user registered is automatically an administrator. Others are just registered but have no access. If you fear for your app security or do not want to check by hand all the users that should automatically be admin add here a list of admin emails. *default: ()* (empty).
* **CORS\_MAX\_AGE**: Integer. This indicates how long the results of a preflight request can be cached in seconds. *default: 1728000* (20 days).

So the minimal settings you have to set are the `SECRET_KEY` and the `MONGODB_SETTINGS` if Comimoc back and front are accessible from the same domain. Add `CORS_ALLOW_ORIGIN_WHITELIST` if they are not.

## use it

For getting and posting comments, best is to use it with Comimoc Front which is an AngularJS application easily customisable.

The admin GUI is available at `/admin` and should ask to register a user the first time you go on it. The first user registered will be an admin by default, unless you set a list of allowed administrators email, in this case, only matching user will be set as administrator.

## develop my own front-end

The API is very simple for now:

* `GET /comments?website=''&page=''` should return all comments matching the page for the website id given.

```javascript
{
    comments: [...]
}
```

* `POST /comments` should return the saved comment.

```javascript
{
  "id": "522cba7897b60e713cd1bae5",
  "page": "/cool_story_bro.html",
  "website": "www.domain.com",
  "author_email": "d10ca8d11301c2f4993ac2279ce4b930", // md5 gravatar suitable email
  "author_name": "Jérôme Steunou",                    // author name
  "author_website": null,                             // author website (not mandatory)
  "content": "Indeed.",                               // the comment itself
  "when": "Sun, 08 Sep 2013 17:57:12 GMT"             // datetime in RTC 822 see http://tools.ietf.org/html/rfc822.html
}
```


# Why Comimoc?

Comimoc stands for **COM**ments **I**n **M**y **O**wn **C**loud. As I create my [blog](http://jeromesteunou.net) with [Pelican](http://docs.getpelican.com/) to keep the control on my content and also having a very simple system with tools I know very well (Python and Github) I wanted the same for my comments. But I did not find it. A lot of people goes for Disqus but I think it is giving to much data and control. So I create Comimoc which is very simple, light and can be run on your own server or at Heroku or at Red Had Cloud OpenShift, etc. And for nothing! For a simple blog, running Comimoc on PaaS services cost nothing and you can backup your comments everyday.

So that's it, I wrote it and I am sharing it so everyone can use it and keep control on their own data.


# Source code

You can access the source code at: https://github.com/JSteunou/comimoc-back

Feel free to dive in, hack in, contribute or ask features (You can ask, I might not add it).
