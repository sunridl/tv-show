from app import app, views

app.add_url_rule('/', view_func=views.global_index)

app.add_url_rule('/users/register', view_func=views.user_register, methods=['GET', 'POST'])
app.add_url_rule('/users/login', view_func=views.user_login, methods=['GET', 'POST'])
app.add_url_rule('/users/logout', view_func=views.user_logout, methods=['GET', 'POST'])
app.add_url_rule('/users/<int:user_id>', view_func=views.user_show, methods=['GET', 'POST'])
app.add_url_rule('/users/<int:user_id>/favourites/shows/edit', view_func=views.favourite_shows_edit, methods=['GET', 'POST'])
app.add_url_rule('/users/<int:user_id>/favourites/channels/edit', view_func=views.favourite_channels_edit, methods=['GET', 'POST'])

app.add_url_rule('/channels_list/', view_func=views.channels_list_index, methods=['GET', 'POST'])
app.add_url_rule('/channels_list/create', view_func=views.channels_list_create, methods=['GET', 'POST'])
app.add_url_rule('/channels_list/<int:channels_list_id>', view_func=views.channels_list_show, methods=['GET', 'POST'])
app.add_url_rule('/channels_list/<int:channels_list_id>/edit', view_func=views.channels_list_edit, methods=['GET', 'POST'])

app.add_url_rule('/channels/', view_func=views.channel_index, methods=['GET', 'POST'])
app.add_url_rule('/channels/create', view_func=views.channel_create, methods=['GET', 'POST'])
app.add_url_rule('/channels/<int:channel_id>', view_func=views.channel_show, methods=['GET', 'POST'])
app.add_url_rule('/channels/<int:channel_id>/edit', view_func=views.channel_edit, methods=['GET', 'POST'])

app.add_url_rule('/shows/', view_func=views.show_index, methods=['GET', 'POST'])
app.add_url_rule('/shows/create', view_func=views.show_create, methods=['GET', 'POST'])
app.add_url_rule('/shows/<int:show_id>', view_func=views.show_show, methods=['GET', 'POST'])
app.add_url_rule('/shows/<int:show_id>/edit', view_func=views.show_edit, methods=['GET', 'POST'])


if __name__ == '__main__':
    app.run(debug=True)
