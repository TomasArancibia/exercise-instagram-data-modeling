import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String(20), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(80), nullable=False)
    name = Column(String(20), nullable=False)
    lastname = Column(String(20))
    age = Column(Integer, nullable=False)


    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "name": self.name,
            "lastname": self.lastname,
            "age": self.age
        }


class Follower(Base):
    __tablename__ = "follower"
    id = Column(Integer, primary_key=True)
    user_from_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user_to_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    def serialize(self):
        return {
            "user_from_id": self.user_from_id,
            "user_to_id": self.user_to_id
        }


class Feed(Base):
    __tablename__ = "feed"
    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "type": self.type
        }


class Location(Base):
    __tablename__ = "location"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    city = Column(String, nullable=False)
    country = Column(String, nullable=False)
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "city": self.city,
            "country": self.country
        }


class Post(Base):
    __tablename__ = "post"
    id = Column(Integer, primary_key=True)
    description = Column(String(400), nullable=False)
    likecount = Column(Integer)
    source_url = Column(String, nullable=False)
    date = Column(String, nullable=False)
    location = Column(Integer, ForeignKey("location.id"), nullable=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    feed_id  = Column(Integer, ForeignKey('feed.id'), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "like_count": self.likecount,
            "location": self.location,
            "date": self.date,
            "source_url": self.source_url
        }


class Comment(Base):
    __tablename__ = "comment"
    id = Column(Integer, primary_key=True)
    text = Column(String(400), nullable=True)
    author_id  = Column(Integer, ForeignKey('user.id'), nullable=False)
    post_id  = Column(Integer, ForeignKey("post.id"), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "text": self.text,
            "author_id": self.author_id,
            "post_id": self.post_id
        }


class Media(Base):
    __tablename__ = "media"
    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)
    url = Column(String, nullable=False)
    post_id = Column(Integer, ForeignKey("post.id"), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "type": self.type,
            "url": self.url,
            "post_id": self.post_id
        }


class Like(Base):
    __tablename__ = "like"
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey("post.id"), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    
    def serialize(self):
        return {
            "user_id": self.user_id,
            "post_id": self.post_id
        }

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
