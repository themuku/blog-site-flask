from flask import render_template
from models import Blog


def home_page():
    blogs = Blog.query.all()

    return render_template("home_page/index.html", blogs=list(blogs)[:3])


def about_page():
    return render_template("about.html")