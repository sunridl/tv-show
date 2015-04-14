from app import app, views

app.add_url_rule('/', view_func=views.global_index)
app.add_url_rule('/users/login', view_func=views.user_login)

if __name__ == '__main__':
    app.run(debug=True)
