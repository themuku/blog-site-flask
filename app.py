from flask import request, redirect, session, render_template, url_for
import bcrypt
from config import db, app
from models import Blog, User
from werkzeug.exceptions import NotFound, Unauthorized, BadRequest, Conflict, InternalServerError


@app.route('/')
def home_page():  # put application's code here
    return render_template("home_page/index.html")


@app.route("/about")
def about_page():
    return render_template("about.html")


@app.route("/blogs/<int:blog_id>")
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
def blogs_page():
    try:
        blogs = Blog.query.all()
        return render_template("blogs_page/index.html", blogs=list(blogs))
    except Exception as e:
        print(str(e))
        return InternalServerError


@app.route("/auth/login", methods=["GET", "POST"])
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
def logout():
    del session["user_id"]

    return redirect(url_for("home_page"))


@app.route("/auth/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]

        exist_email = User.query.filter_by(email=email).first()
        exist_username = User.query.filter_by(username=username).first()

        if exist_email:
            raise Conflict(description="User with this email is already exists")

        if exist_username:
            return Conflict(description="User with this username is already exists")

        hashed_pass = bcrypt.hashpw(password.encode("utf-8"), salt=bcrypt.gensalt())

        new_user = User(username=username, password_hash=hashed_pass.decode("utf-8"), email=email)
        db.session.add(new_user)

        if new_user:
            try:
                db.session.commit()
                session["user_id"] = new_user.id
                return redirect(url_for("login"))
            except Exception as e:
                print(e)
                raise InternalServerError(description="Something went wrong", response=redirect(url_for("home_page")))
        else:
            raise InternalServerError(description="Something went wrong", response=redirect(url_for("home_page")))
    elif request.method == "GET":
        return render_template("auth_page/sign-up.html")


@app.route("/create-post", methods=["POST", "GET"])
def create_post():
    if request.method == "POST":
        title = request.form["title"]
        subtitle = request.form["subtitle"]
        text = request.form["text"]

        if "user_id" in session:
            user = User.query.get(session["user_id"])

            new_blog = Blog(title=title, subtitle=subtitle, author_name=user.username, text=text, user_id=user.id)
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


@app.route("/not-found")
def not_found_page():
    return render_template("not_found_page/index.html")


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)  # during development
