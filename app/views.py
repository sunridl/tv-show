# -*- coding: utf-8 -*-
from flask import url_for, render_template, request
from flask.ext.login import logout_user, login_user, current_user, login_required
from forms import LoginForm
from werkzeug.utils import redirect

from app.models import User, FavouriteChannelsListItem, FavouriteShowsListItem
from app.models import TVShow, TVChannel, TVChannelItem, ChannelsList, ChannelsListItem


@login_required
def global_index():
    return "Hello!"


def user_login():
    if current_user is not None and current_user.is_authenticated():
        return redirect(url_for('global_index'))
    form = LoginForm(request.form)
    if form.validate_on_submit():
        login = form.login.data
        password = form.password.data
        user = User.query.filter_by(nickname=login).first()
        if user.password == password:
            login_user(user, form.remember_me.data)
            return 'ok'

    return render_template('user_login.html', title='Sign In', form=form)


@login_required
def user_logout():
    logout_user()
    return redirect(url_for('global_index'))
