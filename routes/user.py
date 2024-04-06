from flask import render_template, request, redirect, url_for, session, make_response, jsonify
from werkzeug.exceptions import InternalServerError
from models import User, Friend
from config import db


def user_page(username):
    if "user_id" in session:
        user = User.query.filter_by(username=username).first()
        return render_template("user_page/index.html", user=user)
    else:
        return redirect(url_for("login"))


def user_settings_page(username):
    if "user_id" in session:
        user = User.query.filter_by(username=username).first()
        if request.method == "POST":
            user.username = request.form["username"]
            user.email = request.form["email"]
            user.profile_img = request.files["profile_img"]
            user.bio = request.form["bio"]
            db.session.commit()
            return redirect(url_for("user_page", username=user.username))
        elif request.method == "GET":
            return render_template("user_page/settings.html", user=user)


def user_friends_page(username):
    if "user_id" in session:
        user = User.query.get(session["user_id"])
        friend = User.query.filter_by(username=username).first()
    else:
        return redirect(url_for("login"))

    if request.method == "POST":
        friends = Friend.query.filter_by(user_id=user.id, friend_id=friend.id).all()

        if friends:
            return InternalServerError(description="Friendship already exists", response=redirect(url_for("user_friends_page", username=user.username)))
        else:
            new_friend = Friend(user_id=user.id, friend_id=friend.id)

        try:
            db.session.add(new_friend)
            db.session.commit()
        except Exception as e:
            print(str(e))
            return InternalServerError(description="Something went wrong", response=redirect(url_for("user_friends_page", username=user.username)))
        return redirect(url_for("user_friends_page", username=user.username))
    elif request.method == "GET":
        friends = Friend.query.filter_by(user_id=user.id).all()
        users = [User.query.get(friend.friend_id) for friend in friends]
        friends_list = [user.serialize() for user in users]
        return render_template("user_page/friends.html", user=user, friends=friends_list)


def search_page(username):
    if request.method == "GET":
        found_users = User.query.filter_by(username=username).first()  # Fetch the user, if any

        if found_users:
            return make_response(jsonify(found_users.serialize()), 200, {"Content-Type": "application/json"})
        else:
            return make_response(jsonify({"message": "User not found."}), 404)  # Handle not found case
    else:
        return redirect(url_for("home_page"))