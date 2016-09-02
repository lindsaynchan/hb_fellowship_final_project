"""Models and database functions for Final project."""

#importing SQLAlchemy from flask_sqlalchemy library
from flask_sqlalchemy import SQLAlchemy
import bcrypt

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

        user = User.query.filter(User.email==email).first()
        return user

    @classmethod
    def add_user(cls, email, password):
        """Add new user to the database."""

        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()

    @classmethod
    def find_user_id_with_email(cls, email):
        """Find user id using user's email."""

        user_id = db.session.query(User.user_id).filter(User.email==email).one()
        return user_id

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

    @classmethod
    def find_show_with_guidebox_id(cls, guidebox_id):
        """Find show using guidebox_id."""

        show = Show.query.filter(Show.guidebox_id==guidebox_id).one()
        return show

    @classmethod
    def add_show(cls, show_info):
        """Add show to the database."""

        show = Show(guidebox_id=show_info["id"],
            title=show_info["title"],
            artwork_urls=show_info["artwork_608x342"],
            first_aired=show_info["first_aired"],
            description=show_info["overview"])
        db.session.add(show)
        db.session.commit()

    @classmethod
    def add_description_network_to_show(cls, show, show_data):
        """Add description and network to show in database."""

        show.description = show_data["overview"]
        show.network = show_data["network"]
        db.session.commit()

    def as_dict(self):
        """Create dictionary for show information."""

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

    @classmethod
    def find_show_favorites_list(cls, guidebox_id, user_id):
        """Find show in favorites table."""
        
        favorite = Favorite.query.filter_by(guidebox_id=guidebox_id, user_id=user_id).all()
        return favorite

    @classmethod
    def add_to_favorites(cls, guidebox_id, user_id):
        """Add show to favorites table."""

        favorite = Favorite(guidebox_id=guidebox_id, user_id=user_id)
        db.session.add(favorite)
        db.session.commit()

    @classmethod
    def delete_favorite(cls, guidebox_id):

        Favorite.query.filter_by(guidebox_id=guidebox_id).delete()
        db.session.commit()

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

def example_data():
    """Create some sample data for testing."""

    # Empty out existing data if testing has run multiple times.
    User.query.delete()
    Show.query.delete()
    Favorite.query.delete()

    show1 = Show(guidebox_id='6959',
            title=unicode('Game of Thrones'),
            artwork_urls='http://static-api.guidebox.com/thumbnails_xlarge/6959-119520328-608x342.jpg',
            description=unicode("Seven noble families fight for control of the mythical land of Westeros. Friction between the houses leads to full-scale war. All while a very ancient evil awakens in the farthest north. Amidst the war, a neglected military order of misfits, the Night's Watch, is all that stands between the realms of men and the icy horrors beyond."),
            first_aired="2011-04-17")
    show2 = Show(guidebox_id='8521',
            title=unicode('Mad Men'),
            artwork_urls='http://static-api.guidebox.com/091414/thumbnails_xlarge/8521-8744411319-608x342-show-thumbnail.jpg')
    show3 = Show(guidebox_id='169',
                title=unicode('Modern Family'),
                artwork_urls='http://static-api.guidebox.com/091414/thumbnails_xlarge/169-6227865671-608x342-show-thumbnail.jpg')
    show4 = Show(guidebox_id='67',
                title=unicode('American Dad!'),
                artwork_urls='http://static-api.guidebox.com/thumbnails_xlarge/67-1053925115-608x342.jpg',)

    hashed_password = bcrypt.hashpw("hello", bcrypt.gensalt())
    user1 = User(email="hello@hello.com", password=hashed_password)

    favorite1 = Favorite(guidebox_id='67',
                         user_id='1')
    favorite2 = Favorite(guidebox_id='169',
                         user_id='1')

    db.session.add(show1)
    db.session.add(show2)
    db.session.add(show3)
    db.session.add(show4)
    db.session.add(user1)
    db.session.add(favorite1)
    db.session.add(favorite2)
    db.session.commit()

##################################################################


def connect_to_db(app, db_uri="postgresql:///television"):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)



if __name__ == "__main__":
    # able to work with the database directly.
    from server import app
    connect_to_db(app)
    print "Connected to DB."

