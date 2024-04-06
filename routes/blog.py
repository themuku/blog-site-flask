from flask import render_template, request, session, redirect, url_for
from werkzeug.exceptions import InternalServerError, NotFound, Unauthorized
from models import Blog, User
import cloudinary.uploader
from config import db



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


def blogs_page():
    try:
        blogs = Blog.query.all()
        return render_template("blogs_page/index.html", blogs=list(blogs))
    except Exception as e:
        print(str(e))
        return InternalServerError


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
