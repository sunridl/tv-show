import hashlib
from app import db
from sqlalchemy import event, Interval, DateTime
from sqlalchemy import Integer, String, Boolean


# ################################# #
# ########## User MODELS ########## #
# ################################# #


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(Integer, primary_key=True)
    nickname = db.Column(String(80), unique=True, nullable=False)
    password = db.Column(String(64))
    email = db.Column(String(200), index=True, unique=True, nullable=False)
    admin = db.Column(Boolean, default=False, nullable=False)

    favourite_channels = db.relationship('FavouriteChannelsListItem', backref='user')
    favourite_shows = db.relationship('FavouriteShowsListItem', backref='user')

    def __init__(self, nickname, password, email, is_admin=False):
        self.nickname = nickname
        self.password = password
        self.email = email
        self.admin = is_admin

    def check_password(self, password):
        return self.password == hashlib.md5(password).hexdigest()

    def is_admin(self):
        return self.admin == True

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r, %r>' % (self.nickname, self.email)


@event.listens_for(User.password, 'set', retval=True)
def password_change_listener(target, value, oldvalue, initiator):
    value = hashlib.md5(value).hexdigest() if value else value
    return value


class FavouriteChannelsListItem(db.Model):
    __tablename__ = 'favourite_channels_list_item'

    id = db.Column(Integer, primary_key=True)

    channel_id = db.Column(Integer, db.ForeignKey('tvchannel.id'), index=True, nullable=False)
    user_id = db.Column(Integer, db.ForeignKey('user.id'), index=True, nullable=False)
    channel = db.relationship('TVChannel')

    def __init__(self, channel_id, user_id):
        self.channel_id = channel_id
        self.user_id = user_id


class FavouriteShowsListItem(db.Model):
    __tablename__ = 'favourite_shows_list_item'

    id = db.Column(Integer, primary_key=True)

    show_id = db.Column(Integer, db.ForeignKey('tvshow.id'), index=True, nullable=False)
    user_id = db.Column(Integer, db.ForeignKey('user.id'), index=True, nullable=False)
    show = db.relationship('TVShow')

    def __init__(self, show_id, user_id):
        self.show_id = show_id
        self.user_id = user_id


# ################################### #
# ########## TVShow MODELS ########## #
# ################################### #


class TVShow(db.Model):
    __tablename__ = 'tvshow'

    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(250), unique=True, nullable=False)
    duration = db.Column(Interval, nullable=False)

    timetable = db.relationship('TVChannelItem', backref='show')

    def __init__(self, name, duration):
        self.name = name
        self.duration = duration


class TVChannel(db.Model):
    __tablename__ = 'tvchannel'

    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(80), unique=True, index=True, nullable=False)

    timetable = db.relationship('TVChannelItem', backref='channel')

    def __init__(self, name):
        self.name = name


class TVChannelItem(db.Model):
    __tablename__ = 'tvchannel_item'

    id = db.Column(Integer, primary_key=True)
    start_time = db.Column(DateTime, nullable=False)

    show_id = db.Column(Integer, db.ForeignKey('tvshow.id'), index=True, nullable=False)
    channel_id = db.Column(Integer, db.ForeignKey('tvchannel.id'), index=True, nullable=False)

    def __init__(self, start_time, show_id, channel_id):
        self.start_time = start_time
        self.show_id = show_id
        self.channel_id = channel_id


class ChannelsListItem(db.Model):
    __tablename__ = 'channels_list_item'

    id = db.Column(Integer, primary_key=True)

    channels_list_id = db.Column(Integer, db.ForeignKey('channels_list.id'), index=True, nullable=False)
    channel_id = db.Column(Integer, db.ForeignKey('tvchannel.id'), index=True, nullable=False)

    channel = db.relationship('TVChannel')

    def __init__(self, channels_list_id, channel_id):
        self.channels_list_id = channels_list_id
        self.channel_id = channel_id


class ChannelsList(db.Model):
    __tablename__ = 'channels_list'

    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(80), unique=True, index=True, nullable=False)

    channels = db.relationship('ChannelsListItem', backref='channels_list')

    def __init__(self, name):
        self.name = name
