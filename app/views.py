# -*- coding: utf-8 -*-
from functools import wraps
import datetime
from datetime import datetime as dt
from app import db, lm
from flask import url_for, render_template, request, current_app
from flask.ext.login import logout_user, login_user, current_user, login_required
from forms import LoginForm, RegisterForm, TVChannelForm, TVShowForm, ChannelsListForm, FavouriteShowsForm, \
    FavouriteChannelsForm, TVChannelItemForm, SearchForm
from werkzeug.utils import redirect

from app.models import User, FavouriteChannelsListItem, FavouriteShowsListItem
from app.models import TVShow, TVChannel, TVChannelItem, ChannelsList, ChannelsListItem


class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)


def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user or not current_user.is_admin():
            return current_app.login_manager.unauthorized()
        return func(*args, **kwargs)

    return decorated_view


# ################################# #
# ######### Global VIEWS ########## #
# ################################# #


@login_required
def global_index():
    form = SearchForm(request.form)
    timetable = TVChannelItem.query

    if form.validate_on_submit():
        if form.channel_name.data:
            channels = TVChannel.query.filter(TVChannel.name.contains(form.channel_name.data)).all()
            timetable = timetable.filter(TVChannelItem.channel_id.in_(c.id for c in channels))

        if form.show_name.data:
            shows = TVShow.query.filter(TVShow.name.contains(form.show_name.data)).all()
            timetable = timetable.filter(TVChannelItem.show_id.in_(s.id for s in shows))

        if form.time_from.data and form.time_to.data:
            f = form.time_from.data
            t = form.time_to.data
            timetable = timetable.filter(TVChannelItem.start_time.between(f, t))

    timetable = timetable.order_by(TVChannelItem.start_time).all()

    return render_template('global_index.html', timetable=timetable, form=form)


# ################################# #
# ########## User VIEWS ########### #
# ################################# #


def user_register():
    form = RegisterForm(request.form)

    if form.validate_on_submit():
        login_taken = db.session.query(db.exists().where(User.nickname == form.nickname.data)).scalar()
        email_taken = db.session.query(db.exists().where(User.email == form.email.data)).scalar()

        if login_taken or email_taken:
            if login_taken:
                form.nickname.errors.append(u'Nickname already taken. Please try another one')
            if email_taken:
                form.email.errors.append(u'E-mail already registered. Please try another one')
        else:
            user = User(form.nickname.data, form.password.data, form.email.data)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('global_index'))

    return render_template('user_register.html', form=form)


def user_login():
    if current_user is not None and current_user.is_authenticated():
        return redirect(url_for('global_index'))
    form = LoginForm(request.form)

    if form.validate_on_submit():
        nickname = form.nickname.data
        password = form.password.data
        user = User.query.filter_by(nickname=nickname).first()

        if user is not None and user.check_password(password):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('global_index'))
        else:
            form.nickname.errors.append('Invalid credentials')

    return render_template('user_login.html', title='Sign In', form=form)


@login_required
def user_logout():
    logout_user()
    return redirect(url_for('global_index'))


@login_required
def user_show(user_id):
    user = User.query.get(user_id)
    title = u'No such user' if user is None else user.nickname

    if current_user.id != user.id and not current_user.is_admin():
        return lm.unauthorized()

    return render_template('user_show.html', title=title, user=user)


@login_required
def user_delete(user_id):
    user = User.query.get(user_id)
    for c in user.favourite_channels:
        c.query.delete()
    for s in user.favourite_shows:
        s.query.delete()
    user.query.delete()
    db.session.commit()
    return redirect(url_for('global_index'))


# ################################# #
# ####### Favourites VIEWS ######## #
# ################################# #


@login_required
def favourite_channels_edit(user_id):
    user = User.query.get(user_id)
    if current_user.id != user.id:
        return lm.unauthorized()

    form = FavouriteChannelsForm(formdata=request.form,
                                 obj=Struct(**{'channels': user.favourite_channels})) if user is not None else FavouriteChannelsForm(request.form)

    if form.validate_on_submit():
        favourite_channels = [FavouriteChannelsListItem(c.id, user.id) for c in form.channels.data]
        user.favourite_channels = favourite_channels
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('user_show', user_id=user.id))

    return render_template('favourite_channels_edit.html', form=form, user=user)


@login_required
def favourite_shows_edit(user_id):
    user = User.query.get(user_id)
    if current_user.id != user.id:
        return lm.unauthorized()

    form = FavouriteShowsForm(formdata=request.form,
                              obj=Struct(**{'shows': user.favourite_shows})) if user is not None else FavouriteShowsForm(request.form)

    if form.validate_on_submit():
        favourite_shows = [FavouriteShowsListItem(s.id, user.id) for s in form.shows.data]
        user.favourite_shows = favourite_shows
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('user_show', user_id=user.id))

    return render_template('favourite_shows_edit.html', form=form, user=user)


# ################################# #
# ###### ChannelsList VIEWS ####### #
# ################################# #


def channels_list_index():
    lists = ChannelsList.query.all()
    return render_template('channels_list_index.html', lists=lists)


def channels_list_show(channels_list_id):
    channels_list = ChannelsList.query.get(channels_list_id)
    title = u'No such channels\' list' if channels_list is None else channels_list.name
    return render_template('channels_list_show.html', channels_list=channels_list, title=title)


@login_required
@admin_required
def channels_list_create():
    form = ChannelsListForm(request.form)

    if form.validate_on_submit():
        channels_list = ChannelsList(name=form.name.data)
        channels_list.channels = [ChannelsListItem(channels_list.id, c.id) for c in form.channels.data]
        db.session.add(channels_list)
        db.session.commit()
        return redirect(url_for('channels_list_show', channels_list_id=channels_list.id))

    return render_template('channels_list_edit.html', form=form)


@login_required
@admin_required
def channels_list_edit(channels_list_id):
    channels_list = ChannelsList.query.get(channels_list_id)
    form = ChannelsListForm(formdata=request.form, obj=channels_list)

    if form.validate_on_submit():
        db.session.add(channels_list)
        db.session.commit()
        return redirect(url_for('channels_list_show', channels_list_id=channels_list.id))

    return render_template('channels_list_edit.html', form=form)


@login_required
@admin_required
def channels_list_delete(channels_list_id):
    channels_list = ChannelsList.query.get(channels_list_id)
    for c in channels_list.channels:
        c.query.delete()
    channels_list.query.delete()
    db.session.commit()
    return redirect(url_for('channel_index'))


# ################################# #
# ######## Channel VIEWS ########## #
# ################################# #


def channel_index():
    channels = TVChannel.query.all()
    return render_template('channel_index.html', channels=channels)


def channel_show(channel_id):
    channel = TVChannel.query.get(channel_id)
    title = u'No such channel' if channel is None else channel.name
    return render_template('channel_show.html', channel=channel, title=title)


@login_required
@admin_required
def channel_create():
    form = TVChannelForm(request.form)

    if form.validate_on_submit():
        channel = TVChannel(form.name.data)
        db.session.add(channel)
        db.session.commit()
        return redirect(url_for('channel_show', channel_id=channel.id))

    return render_template('channel_edit.html', form=form)


@login_required
@admin_required
def channel_edit(channel_id):
    channel = TVChannel.query.get(channel_id)
    form = TVChannelForm(formdata=request.form, obj=channel)

    if form.validate_on_submit():
        db.session.add(channel)
        db.session.commit()
        return redirect(url_for('channel_show', channel_id=channel.id))

    return render_template('channel_edit.html', form=form)


@login_required
@admin_required
def channel_delete(channel_id):
    channel = TVChannel.query.get(channel_id)

    item_ids = [item.id for item in channel.timetable]
    TVChannelItem.query.filter(TVChannelItem.channel_id.in_(item_ids)).delete()

    FavouriteChannelsListItem.query.filter_by(channel_id=channel.id).delete()
    ChannelsListItem.query.filter_by(channel_id=channel.id).delete()

    TVChannel.query.filter_by(id=channel_id).delete()
    db.session.commit()

    return redirect(url_for('channel_index'))


# ######################################## #
# ########## ChannelItem VIEWS ########### #
# ######################################## #


@login_required
@admin_required
def channel_item_create(channel_id):
    channel = TVChannel.query.get(channel_id)
    form = TVChannelItemForm(request.form)

    if form.validate_on_submit():
        start_time = form.start_time.data
        channel.timetable.append(TVChannelItem(start_time, form.show.data.id, channel.id))
        db.session.add(channel)
        db.session.commit()
        return redirect(url_for('channel_show', channel_id=channel.id))

    return render_template('channel_item_edit.html', form=form, channel=channel)


@login_required
@admin_required
def channel_item_edit(channel_id, item_id):
    channel_item = TVChannelItem.get(item_id)
    form = TVChannelItemForm(formdata=request.form, obj=channel_item)

    if form.validate_on_submit():
        channel_item.start_time = dt.strptime(form.start_time.data, '%d.%m.%Y %H:%M')
        channel_item.show = form.show.data.id
        db.session.add(channel_item)
        db.session.commit()
        return redirect(url_for('channel_show', channel_id=channel_id))

    channel = channel_item.channel if channel_item is not None else None
    return render_template('channel_item_edit.html', form=form, channel=channel)


@login_required
@admin_required
def channel_item_delete(channel_id, item_id):
    TVChannelItem.filter_by(id=item_id).delete()
    db.session.commit()
    return redirect(url_for('channel_show', channel_id=channel_id))


# ################################# #
# ########## Show VIEWS ########### #
# ################################# #


def show_index():
    shows = TVShow.query.all()
    return render_template('show_index.html', shows=shows)


def show_show(show_id):
    show = TVShow.query.get(show_id)
    title = u'No such TV-show' if show is None else show.name
    return render_template('show_show.html', show=show, title=title)


@login_required
@admin_required
def show_create():
    form = TVShowForm(request.form)

    if form.validate_on_submit():
        duration = datetime.timedelta(minutes=form.duration.data)
        show = TVShow(form.name.data, duration)
        db.session.add(show)
        db.session.commit()
        return redirect(url_for('show_show', show_id=show.id))

    return render_template('show_edit.html', form=form)


@login_required
@admin_required
def show_edit(show_id):
    show = TVShow.query.get(show_id)
    form = TVShowForm(obj=show)

    if form.validate_on_submit():
        db.session.add(show)
        db.session.commit()
        return redirect(url_for('show_show', show_id=show.id))

    return render_template('show_edit.html', form=form)


@login_required
@admin_required
def show_delete(show_id):
    show = TVShow.query.get(show_id)

    for item in show.timetable:
        TVChannelItem.query.filter_by(show_id=item.id).delete()

    FavouriteShowsListItem.query.filter_by(show_id=show.id).delete()

    TVShow.query.filter_by(id=show.id).delete()
    db.session.commit()

    return redirect(url_for('channel_index'))
