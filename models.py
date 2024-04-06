from config import db
from datetime import datetime
from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from enums import EnumRole, EnumNotificationCategory, EnumStatus


class Notification(db.Model):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    message = Column(String(255), nullable=False)
    category = Column(Enum(EnumNotificationCategory), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "<Notification %r>" % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "message": self.message,
            "created_at": self.created_at,
            "category": self.category,
        }


class Friend(db.Model):
    __tablename__ = "friends"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    friend_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(Enum(EnumStatus), default=EnumStatus.PENDING)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "<Friend %r>" % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "friend_id": self.friend_id,
            "created_at": self.created_at,
            "status": self.status,
        }


class User(db.Model):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    blogs = db.relationship("Blog", backref="author")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    role = Column(Enum(EnumRole), default=EnumRole.USER)
    profile_img = Column(String(255), default="default.jpg")
    friends = db.relationship("Friend", backref="user", foreign_keys=[Friend.user_id])
    bio = Column(Text, nullable=True)

    def __repr__(self):
        return "<User %r>" % self.id

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "profile_img": self.profile_img,
            "role": self.role,
            "created_at": self.created_at,
            "bio": self.bio,
            "friends": self.friends,
            "blogs": self.blogs
        }


class Blog(db.Model):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    author_name = Column(String(100), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    subtitle = Column(String(255), nullable=False)
    text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    blog_img = Column(String(255), default="default.jpg")

    def __repr__(self):
        return "<BlogPost %r>" % self.id

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "author_name": self.author_name,
            "subtitle": self.subtitle,
            "text": self.text,
            "created_at": self.created_at,
            "blog_img": self.blog_img,
            "user_id": self.user_id
        }
