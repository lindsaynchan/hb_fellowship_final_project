"""Models and database functions for Final project."""

#importing SQLAlchemy from flask_sqlalchemy library
from flask_sqlalchemy import SQLAlchemy

#setting up our database
db = SQLAlchemy()

##################################################################

class User(db.Model):
    """Creating users table."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, 
                           primary_key=True,
                           autoincrement=True)
    username = db.Column(db.String(20),
                         unique=True,
                         nullable=False)
    email = db.Column(db.String(64),
                      unique=True,
                      nullable=False)
    password = db.Column(db.String(20),
                         nullable=False)


class Show(db.Model):
    """Creating TV shows table."""

    __table__ = "shows"

    show_id = db.Column(db.Integer, 
                       primary_key=True,
                       autoincrement=True)
    title = db.Column(db.Unicode(100),
                      nullable=False)
    description = db.Column(db.UnicodeText,
                            nullable=True)
    seasons = db.Column(db.String(20),
                        nullable=True)


class Service(db.Model):
    """Creating streaming services table."""

    __tablename__ = "services"

    service_id = db.Column(db.Integer, 
                           primary_key=True,
                           autoincrement=True)
    name = db.Column(db.String(50),
                     nullable=False)


class Favorite(db.Model):
    """Creating favorite shows table."""

    __tablename__ = "favorites"

    favorite_id = db.Column(db.Integer, 
                            primary_key=True,
                            autoincrement=True)
    show_id = db.Column(db.Integer,
                        db.ForeignKey('shows.show_id'),
                        nullable=False)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'),
                        nullable=False)

    show = db.relationship("Show", backref="favorites")
    user = db.relationship("User", backref="favorites")


class Cable(db.Model):
    """Creating cable service listings table."""

    __tablename__ = "cables"

    cable_id = db.Column(db.Integer, 
                         primary_key=True,
                         autoincrement=True)
    show_id = db.Column(db.Integer,
                        db.ForeignKey('shows.show_id'),
                        nullable=False)
    date = db.Column(db.Datetime,
                     nullable=False)
    time = db.Column(db.Datetime,
                     nullable=False)
    network = db.Column(db.String(50),
                        nullable=False)

    show = db.relationship("Show", backref="cables")


class Streaming(db.Model):
    """Creating streaming availabilities table."""

    __tablename__ = "streamings"

    streaming_id = db.Column(db.Integer,
                             primary_key=True,
                             autoincrement=True)
    show_id = db.Column(db.Integer,
                        db.ForeignKey('shows.show_id'),
                        nullable=False)
    service_id = db.Column(db.Integer, 
                           db.ForeignKey('services.service_id'),
                           nullable=False)

    show = db.relationship("Show", backref="streamings")
    service = db.relationship("Service", backref="streamings")

##################################################################

def init_app():
    # So that we can use Flask-SQLAlchemy, we'll make a Flask app
    from flask import Flask
    app = Flask(__name__)

    connect_to_db(app)
    print "Connected to DB."

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///television'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will
    # leave you in a state of being able to work with the database
    # directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."