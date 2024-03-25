from flask import Flask, request, make_response, redirect, session, jsonify, render_template
import bcrypt

from config import db, app

from models import Blog, User


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
            return redirect("/not-found")
    except Exception as e:
        print(str(e))
        return redirect("/not-found")


@app.route("/blogs")
def blogs_page():
    try:
        blogs = Blog.query.all()
        return render_template("blogs_page/index.html", blogs=list(blogs))
    except Exception as e:
        print(str(e))
        return "Something went wrong"


@app.route("/auth/<string:auth>", methods=["GET", "POST"])
def auth_page(auth):
    if request.method == "GET":
        if auth == "login":
            return render_template("auth_page/login.html")
        elif auth == "sign-up":
            return render_template("auth_page/sign-up.html")
    elif request.method == "POST":
        if auth == "sign-up":
            name = request.form["username"]
            password = request.form["password"]
            email = request.form["email"]

            hashed_pass = bcrypt.hashpw(password.encode("utf-8"), salt=bcrypt.gensalt())

            new_user = User(name=name, password_hash=hashed_pass.decode("utf-8"), email=email)
            db.session.add(new_user)

            if new_user:
                try:
                    db.session.commit()
                    session["user_id"] = new_user.id
                    return redirect("/auth/login")
                except Exception as e:
                    print(e)
                    redirect("/not-found")
            else:
                return redirect("/not-found")

        elif auth == "login":
            email = request.form["email"]
            password = request.form["password"]

            found_user = User.query.filter(User.email.like(f"%{email}%")).first()

            if found_user and bcrypt.checkpw(password.encode("utf-8"), found_user.password_hash.encode("utf-8")):
                session["user_id"] = found_user.id
                return redirect("/")
            else:
                return {'errors': ['Invalid username or password. Please try again.']}, 401


@app.route("/create-post", methods=["POST", "GET"])
def create_post():
    if request.method == "POST":
        title = request.form["title"]
        subtitle = request.form["subtitle"]
        author_name = request.form["author-name"]
        text = request.form["text"]

        new_blog = Blog(title=title, subtitle=subtitle, author_name=author_name, text=text, user_id=session["user_id"])

        db.session.add(new_blog)

        try:
            db.session.commit()
            last_post = Blog.query.order_by(Blog.created_at.desc()).first()

            return redirect(f"/blogs/{last_post.id}")
        except Exception as e:
            print(str(e))
            return redirect("/not-found")
    elif request.method == "GET":
        return render_template("blogs_page/create_post.html")


@app.route("/not-found")
def not_found_page():
    return render_template("not_found_page/index.html")


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)  # during development
