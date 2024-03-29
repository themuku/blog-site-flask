from config import db
from datetime import datetime
from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey, Enum


class EnumRole:
    ADMIN = "admin"
    USER = "user"


class User(db.Model):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    blogs = db.relationship("Blog", backref="author")
    created_at = Column(DateTime, default=datetime.utcnow)
    role = Column(Enum(EnumRole.ADMIN, EnumRole.USER), default=EnumRole.USER)
    profile_img = Column(String(255), default="default.jpg")

    def __repr__(self):
        return "<User %r>" % self.id


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
