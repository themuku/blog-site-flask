from flask import Flask, render_template, url_for, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import Column, String, Integer, Text, DateTime, delete


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Blog(db.Model):
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    author_name = Column(String(100), nullable=False)
    subtitle = Column(String(255), nullable=False)
    text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "<Article %r>" % self.id


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
        pass


@app.route("/create-post", methods=["POST", "GET"])
def create_post():
    if request.method == "POST":
        title = request.form["title"]
        subtitle = request.form["subtitle"]
        author_name = request.form["author-name"]
        text = request.form["text"]

        new_blog = Blog(title=title, subtitle=subtitle, author_name=author_name, text=text)

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
