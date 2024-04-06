from flask import request, render_template, redirect, url_for, session, flash
from werkzeug.exceptions import BadRequest, Conflict, InternalServerError
import cloudinary.uploader

from enums import EnumRole
from models import User
from config import db
import bcrypt


def login_user():
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


def logout_user():
    del session["user_id"]

    return redirect(url_for("home_page"))


def sign_up_user():
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
