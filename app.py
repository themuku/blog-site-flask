from flask import request, redirect, session, render_template, url_for, flash
import bcrypt
from config import db, app
from models import Blog, User, EnumRole
from werkzeug.exceptions import NotFound, Unauthorized, BadRequest, Conflict, InternalServerError
import cloudinary.uploader
from helpers import inject_user_data


@app.route('/')
@inject_user_data
def home_page():
    blogs = Blog.query.all()

    return render_template("home_page/index.html", blogs=list(blogs)[:3])


@app.route("/about")
@inject_user_data
def about_page():
    return render_template("about.html")


@app.route("/blogs/<int:blog_id>")
@inject_user_data
def single_blog_page(blog_id):
    try:
        found_blog = Blog.query.get(blog_id)
        if found_blog:
            return render_template("blogs_page/single_blog.html", blog=found_blog)
        else:
            raise NotFound
    except Exception as e:
        print(str(e))
        raise InternalServerError


@app.route("/blogs")
@inject_user_data
def blogs_page():
    try:
        blogs = Blog.query.all()
        return render_template("blogs_page/index.html", blogs=list(blogs))
    except Exception as e:
        print(str(e))
        return InternalServerError


@app.route("/auth/login", methods=["GET", "POST"])
@inject_user_data
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        found_user = User.query.filter(User.email.like(f"%{email}%")).first()

        if found_user and bcrypt.checkpw(password.encode("utf-8"), found_user.password_hash.encode("utf-8")):
            session["user_id"] = found_user.id
            return redirect(url_for("home_page"))
        else:
            raise BadRequest(response=redirect(url_for("sign_up")))
    elif request.method == "GET":
        return render_template("auth_page/login.html")


@app.route("/auth/logout")
@inject_user_data
def logout():
    del session["user_id"]

    return redirect(url_for("home_page"))


@app.route("/auth/sign-up", methods=["GET", "POST"])
@inject_user_data
def sign_up():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        profile_img = request.files["profile_img"]

        exist_email = User.query.filter_by(email=email).first()
        exist_username = User.query.filter_by(username=username).first()

        if exist_email:
            raise Conflict(description="User with this email is already exists")

        if exist_username:
            return Conflict(description="User with this username is already exists")

        hashed_pass = bcrypt.hashpw(password.encode("utf-8"), salt=bcrypt.gensalt())

        upload_result = cloudinary.uploader.upload(profile_img, folder="profile_images", resource_type="image")

        new_user = User(username=username, password_hash=hashed_pass.decode("utf-8"), email=email, profile_img=upload_result["url"])
        print(new_user)
        db.session.add(new_user)

        if new_user:
            try:
                db.session.commit()
                session["user_id"] = new_user.id
                return redirect(url_for("login"))
            except Exception as e:
                print(e)
                flash(str(e))
                raise InternalServerError(description="Something went wrong", response=redirect(url_for("home_page")))
        else:
            raise InternalServerError(description="Something went wrong", response=redirect(url_for("home_page")))
    elif request.method == "GET":
        return render_template("auth_page/sign-up.html")


@app.route("/create-post", methods=["POST", "GET"])
@inject_user_data
def create_post():
    if request.method == "POST":
        title = request.form["title"]
        subtitle = request.form["subtitle"]
        text = request.form["text"]
        blog_img = request.files["blog_img"]

        if "user_id" in session:
            user = User.query.get(session["user_id"])

            upload_result = cloudinary.uploader.upload(blog_img, folder="blog_images", resource_type="image")

            new_blog = Blog(title=title, subtitle=subtitle, author_name=user.username, text=text, user_id=user.id, blog_img=upload_result["url"])
        else:
            raise Unauthorized(response=redirect(url_for("login")))

        db.session.add(new_blog)

        try:
            db.session.commit()
            last_post = Blog.query.order_by(Blog.created_at.desc()).first()

            return redirect(f"/blogs/{last_post.id}")
        except Exception as e:
            print(str(e))
            raise InternalServerError(description="Something went wrong", response=redirect(url_for("home_page")))
    elif request.method == "GET":
        return render_template("blogs_page/create_post.html")



@app.route("/admin/create", methods=["POST", "GET"])
def admin_login_page():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        profile_img = request.files["profile_img"]

        exist_email = User.query.filter_by(email=email).first()
        exist_username = User.query.filter_by(username=username).first()

        if exist_email:
            raise Conflict(description="User with this email is already exists")

        if exist_username:
            return Conflict(description="User with this username is already exists")

        hashed_pass = bcrypt.hashpw(password.encode("utf-8"), salt=bcrypt.gensalt())

        upload_result = cloudinary.uploader.upload(profile_img, folder="profile_images", resource_type="image")

        new_user = User(username=username, password_hash=hashed_pass.decode("utf-8"), email=email, profile_img=upload_result["url"], role=EnumRole.ADMIN)
        print(new_user)
        db.session.add(new_user)

        if new_user:
            try:
                db.session.commit()
                session["user_id"] = new_user.id
                return redirect(url_for("login"))
            except Exception as e:
                print(e)
                flash(str(e))
                raise InternalServerError(description="Something went wrong", response=redirect(url_for("home_page")))
        else:
            raise InternalServerError(description="Something went wrong", response=redirect(url_for("home_page")))
    elif request.method == "GET":
        return render_template("auth_page/sign-up.html")


@app.route("/user/<string:username>")
@inject_user_data
def user_page(username):
    if "user_id" in session:
        user = User.query.filter_by(username=username).first()
        return render_template("user_page/index.html", user=user)
    else:
        return redirect(url_for("login"))


@app.route("/user/<string:username>/settings", methods=["POST", "GET"])
@inject_user_data
def user_settings_page(username):
    if "user_id" in session:
        user = User.query.filter_by(username=username).first()
        if request.method == "POST":
            user.username = request.form["username"]
            user.email = request.form["email"]
            user.profile_img = request.files["profile_img"]
            db.session.commit()
            return redirect(url_for("user_page", username=user.username))
        elif request.method == "GET":
            return render_template("user_page/settings.html", user=user)


@app.route("/user/<string:username>/friends", methods=["POST", "GET"])
@inject_user_data
def user_friends_page(username):
    if "user_id" in session:
        user = User.query.filter_by(username=username).first()
    else:
        return redirect(url_for("login"))

    if request.method == "POST":
        friend_username = request.form["friend_username"]
        friend = User.query.filter_by(username=friend_username).first()
        user.friends.append(friend)
        db.session.commit()
        return redirect(url_for("user_friends_page", username=user.username))
    elif request.method == "GET":
        return render_template("user_page/friends.html", user=user)


@app.route("/not-found")
@inject_user_data
def not_found_page():
    return render_template("not_found_page/index.html")


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)  # during development
