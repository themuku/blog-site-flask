# Importing libraries
from flask import redirect, render_template, url_for
from config import db, app
from werkzeug.exceptions import NotFound, Unauthorized, BadRequest, Conflict, InternalServerError
from helpers import inject_user_data

# Importing routes
from routes.home import home_page, about_page
from routes.blog import single_blog_page, blogs_page, create_post
from routes.auth import login_user, logout_user, sign_up_user, admin_login_page
from routes.user import user_page, user_settings_page, user_friends_page, search_page


# Routes
@app.route('/')
@inject_user_data
def home():
    return home_page()


@app.route("/about")
@inject_user_data
def about():
    return about_page()


@app.route("/blogs/<int:blog_id>")
@inject_user_data
def single_blog(blog_id):
    return single_blog_page(blog_id)


@app.route("/blogs")
@inject_user_data
def blogs():
    return blogs_page()


@app.route("/auth/login", methods=["GET", "POST"])
@inject_user_data
def login():
    return login_user()


@app.route("/auth/logout")
@inject_user_data
def logout():
    return logout_user()


@app.route("/auth/sign-up", methods=["GET", "POST"])
@inject_user_data
def sign_up():
    return sign_up_user()


@app.route("/create-post", methods=["POST", "GET"])
@inject_user_data
def create_post():
    return create_post()


@app.route("/admin/create", methods=["POST", "GET"])
def admin_login():
    return admin_login_page()


@app.route("/user/<string:username>")
@inject_user_data
def user_page(username):
    return user_page(username)


@app.route("/user/<string:username>/settings", methods=["POST", "GET"])
@inject_user_data
def user_settings_page(username):
    return user_settings_page(username)


@app.route("/user/<string:username>/friends", methods=["POST", "GET"])
@inject_user_data
def user_friends_page(username):
    return user_friends_page(username)


@app.route("/search/user/<string:username>", methods=["GET"])
def search_page(username):
    return search_page(username)


@app.route("/not-found")
@inject_user_data
def not_found_page():
    return render_template("not_found_page/index.html")


@app.errorhandler(NotFound)
def page_not_found(e):
    return redirect(url_for("not_found_page"))


@app.errorhandler(Unauthorized)
def unauthorized(e):
    return redirect(url_for("login"))


@app.errorhandler(BadRequest)
def bad_request(e):
    return redirect(url_for("sign_up"))


@app.errorhandler(Conflict)
def conflict(e):
    return redirect(url_for("sign_up"))


@app.errorhandler(InternalServerError)
def internal_server_error(e):
    return redirect(url_for("home_page"))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)  # during development
