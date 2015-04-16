from app.models import TVChannel, TVShow
from flask.ext.wtf import Form
from wtforms import BooleanField, StringField, PasswordField, IntegerField, widgets
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField
from wtforms.validators import DataRequired, Length, Email, NumberRange


class LoginForm(Form):
    nickname = StringField('nickname', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)


class RegisterForm(Form):
    nickname = StringField('nickname', validators=[DataRequired(), Length(min=3, max=25)])
    email = StringField('email', validators=[DataRequired(), Email(message=None), Length(min=6, max=40)])
    password = PasswordField('password', validators=[DataRequired(), Length(min=6, max=25)])


class TVChannelForm(Form):
    name = StringField('name', validators=[DataRequired(), Length(min=1, max=80)])


class TVShowForm(Form):
    name = StringField('name', validators=[DataRequired(), Length(min=1, max=80)])
    duration = IntegerField('duration', validators=[DataRequired(), NumberRange(1, 600)])


class ChannelsListForm(Form):
    name = StringField('name', validators=[DataRequired(), Length(min=1, max=80)])
    channels = QuerySelectMultipleField(
        query_factory=TVChannel.query.all,
        get_label=lambda x: x.name,
        widget=widgets.ListWidget(prefix_label=False),
        option_widget=widgets.CheckboxInput()
    )


class FavouriteChannelsForm(Form):
    channels = QuerySelectMultipleField(
        query_factory=TVChannel.query.all,
        get_label=lambda x: x.name,
        widget=widgets.ListWidget(prefix_label=False),
        option_widget=widgets.CheckboxInput()
    )


class FavouriteShowsForm(Form):
    shows = QuerySelectMultipleField(
        query_factory=TVShow.query.all,
        get_label=lambda x: x.name,
        widget=widgets.ListWidget(prefix_label=False),
        option_widget=widgets.CheckboxInput()
    )
