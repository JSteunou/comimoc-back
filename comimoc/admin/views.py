# -*- coding: utf-8 -*-


"""
Flask views that contains Blueprints
"""

from __future__ import unicode_literals


from comimoc.admin.models import User
from comimoc.models import Comment

from flask import flash
from flask import redirect
from flask import url_for

from flask.ext.admin import AdminIndexView
from flask.ext.admin import expose
from flask.ext.admin.contrib.mongoengine import ModelView
from flask.ext.login import current_user
from flask.ext.login import login_user
from flask.ext.login import logout_user

from flask_wtf import Form
from wtforms import fields
from wtforms import validators

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash





class LoginView(AdminIndexView):
    """
    View used for the flask admin index view
    It handles login / logout / register processes
    """
    
    def __init__(self, config, *args, **kwargs):
        """
        Override init to be able to inject flask app config
        """
        self.config = config
        super(LoginView, self).__init__(*args, **kwargs)
    
    @expose('/')
    def index(self):
        """
        Index of admin panel
        Show welcome message or redirect to login or register if no user yet
        """
        # no user? redirect to register
        if not User.objects.first():
            return redirect(url_for('.register'))
        # no user logged in? redirect to login
        if not current_user.is_authenticated():
            return redirect(url_for('.login'))
        # default = index.html
        return self.render("index.html", login=current_user.login, active=current_user.is_active())
    
    @expose('/login', methods=['GET', 'POST'])
    def login(self):
        '''
        Handle login process
        '''
        form = LoginForm()
        if form.validate_on_submit():
            # when form is valid and user exists and password matches...
            user = User.objects(login=form.login.data).first()
            if user is None or not check_password_hash(user.password, form.password.data):
                flash('Invalid login or password')
            else:
                # ... logged in and redirect to index (even not active)
                login_user(user, force=True)
                return redirect(url_for(".index"))
        # default is just show login form
        return self.render('form.html', form=form, title="Sign in")
    
    @expose("/logout")
    def logout(self):
        '''
        Handle logout process
        '''
        # just log out the user, show he is and redirect to index
        logout_user()
        flash("You are now logged out")
        return redirect(url_for(".index"))
    
    @expose('/register', methods=['GET', 'POST'])
    def register(self):
        '''
        Handle registration process
        '''
        # if already authenticated use User panel
        # rather register form
        # (also avoid for not admin account to add user)
        if current_user.is_authenticated():
            return redirect(url_for(".index"))
        
        form = RegistrationForm()
        if form.validate_on_submit():
            user = User()
            form.populate_obj(user)
            self._add_user(user)
            login_user(user, force=True)
            return redirect(url_for('.index'))
        # default is just show register form
        return self.render('form.html', form=form, title="Register")
    
    def _add_user(self, user):
        '''
        Add a user to the DB
        Set the `is_admin` property and encrypts the `password`
        '''
        # make the first registered user an admin by default
        # if no admin emails list set
        if not self.config['ADMIN_EMAILS'] and not User.objects.first():
            user.is_admin = True
        # make the user an admin is belong to the admin emails list
        if user.email in self.config['ADMIN_EMAILS']:
            user.is_admin = True
        # encrypt pwd
        user.password = generate_password_hash(user.password)
        # save into DB
        user.save()





class CommentModelView(ModelView):
    """
    Simple ModelView for Comment Model
    with access restriction
    """
    
    def __init__(self, *args, **kwargs):
        super(CommentModelView, self).__init__(Comment, *args, **kwargs)
    
    def is_accessible(self):
        return current_user.is_authenticated() and current_user.is_active()


class UserModelView(ModelView):
    """
    Simple ModelView for User Model
    with access restriction
    """
    
    def __init__(self, *args, **kwargs):
        super(UserModelView, self).__init__(User, *args, **kwargs)
    
    def is_accessible(self):
        return current_user.is_authenticated() and current_user.is_active()





class LoginForm(Form):
    """
    Flask-WTForm for login
    """
    login = fields.TextField(validators=[validators.DataRequired()])
    password = fields.PasswordField(validators=[validators.DataRequired()])


class RegistrationForm(Form):
    """
    Flask-WTForm for registration
    """
    login = fields.TextField(validators=[validators.DataRequired(), validators.Length(4)])
    email = fields.TextField(validators=[validators.Email(), validators.required()])
    password = fields.PasswordField(validators=[validators.DataRequired(), validators.Length(6)])
    
    def validate_login(self, field):
        if User.objects(login=field.data):
            raise validators.ValidationError("This login is not available.")
    
    def validate_email(self, field):
        if User.objects(email=field.data):
            raise validators.ValidationError("You already are registered.")
