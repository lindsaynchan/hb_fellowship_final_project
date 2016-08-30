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
    email = db.Column(db.String(64),
                      unique=True,
                      nullable=False)
    password = db.Column(db.String(75),
                         nullable=False)

    @classmethod
    def get_user_with_email(cls, email):
        """Search for user in database using given an email address."""

        SELECT = "SELECT * FROM User WHERE email = :email"
        user_search = db.session.execute(cls.SELECT, {'email':email})
        user = cursor.fetchone()
        # user = db.session.query(User).filter(User.email==email).first()
        return user

    def add_user(self, email, password):
        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()

class Show(db.Model):
    """Creating TV shows table."""

    __tablename__ = "shows"

    show_id = db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True)
    guidebox_id = db.Column(db.String(20),
                        unique=True,
                        nullable=False)
    title = db.Column(db.Unicode(100),
                      nullable=False)
    artwork_urls = db.Column(db.String(500),
                        nullable=True)
    first_aired = db.Column(db.Date,
                            nullable=True)
    network = db.Column(db.String(20),
                        nullable=True)
    description = db.Column(db.UnicodeText,
                            nullable=True)
    seasons = db.Column(db.String(20),
                        nullable=True)

    def as_dict(self):

        return {"show_id":self.show_id,"guidebox_id":self.guidebox_id,"title":self.title,"artwork_urls":self.artwork_urls,"first_aired":self.first_aired.year,"network":self.network,"description":self.description,"seasons":self.seasons}


class Favorite(db.Model):
    """Creating favorite shows table."""

    __tablename__ = "favorites"

    favorite_id = db.Column(db.Integer, 
                            primary_key=True,
                            autoincrement=True)
    guidebox_id = db.Column(db.String(20),
                        db.ForeignKey('shows.guidebox_id'),
                        nullable=False)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'),
                        nullable=False)

    show = db.relationship("Show", backref="favorites")
    user = db.relationship("User", backref="favorites")


class Network(db.Model):
    """Creating networks table."""

    __tablename__ = "networks"

    network_id = db.Column(db.Integer, 
                           primary_key=True,
                           autoincrement=True)
    #channel
    channel = db.Column(db.String(20),
                        nullable=False)
    #callSign
    network_name = db.Column(db.String(50),
                             nullable=True)



class CableListing(db.Model):
    """Creating cable service listings table."""

    __tablename__ = "cable_listings"

    cable_listing_id = db.Column(db.Integer, 
                         primary_key=True,
                         autoincrement=True)
    guidebox_id = db.Column(db.String(20),
                        db.ForeignKey('shows.guidebox_id'),
                        nullable=False)
    date = db.Column(db.DateTime,
                     nullable=False)
    time = db.Column(db.DateTime,
                     nullable=False)
    network_id = db.Column(db.Integer,
                        db.ForeignKey('networks.network_id'),
                        nullable=False)

    show = db.relationship("Show", backref="cable_listings")
    network = db.relationship("Network", backref="cable_listings")


class StreamingService(db.Model):
    """Creating streaming services table."""

    __tablename__ = "streaming_services"

    streaming_service_id = db.Column(db.Integer, 
                           primary_key=True,
                           autoincrement=True)
    name = db.Column(db.String(50),
                     nullable=False)


class Streaming(db.Model):
    """Creating streaming availabilities table."""

    __tablename__ = "streamings"

    streaming_id = db.Column(db.Integer,
                             primary_key=True,
                             autoincrement=True)
    guidebox_id = db.Column(db.String(20),
                        db.ForeignKey('shows.guidebox_id'),
                        nullable=False)
    service_id = db.Column(db.Integer, 
                           db.ForeignKey('streaming_services.streaming_service_id'),
                           nullable=False)

    show = db.relationship("Show", backref="streamings")
    service = db.relationship("StreamingService", backref="streamings")

##################################################################


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///television'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)



if __name__ == "__main__":
    # able to work with the database directly.
    from server import app
    connect_to_db(app)
    print "Connected to DB."

