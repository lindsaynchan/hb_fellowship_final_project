"""Television listings and streaming search."""

import os
from jinja2 import StrictUndefined
from flask import Flask, render_template, request, flash, redirect, session, jsonify
from model import connect_to_db, db, User, Show, StreamingService, Favorite, CableListing, Streaming, Network
from guidebox import guidebox_search_title, guidebox_show_info, guidebox_season_info, guidebox_streaming_sources_info
from onconnect import onconnect_search_series_id, onconnect_search_airings
import requests
import urllib2
import arrow
import json
import bcrypt


app = Flask(__name__)

app.secret_key = os.environ.get('APP_KEY')
GUIDEBOX_API_KEY = os.environ.get('GUIDEBOX_API_KEY')
ONCONNECT_API_KEY = os.environ.get('ONCONNECT_API_KEY')

app.jinja_env.undefined = StrictUndefined

GUIDEBOX_BASE_URL = "http://api-public.guidebox.com/v1.43/US/" + GUIDEBOX_API_KEY


##########################################################################


@app.route('/')
def show_index():
    """Homepage."""

    return render_template("homepage.html")


@app.route('/login')
def show_login_page():
    """Login page."""

    return render_template("login.html")


@app.route('/login-user', methods=['POST'])
def login_user():
    """Login user."""

    #get email and password from login form and save as variables
    email = request.form.get("email")
    password = request.form.get("password")

    #run query to check if email and password is correct in the database
    user = User.query.filter(User.email==email).first()

    #if email and password match what's in the system, add user to the session and redirect to homepage
    if bcrypt.checkpw(password, user.password):
        session["current_user"] = email
        print session

        flash("Logged in as %s." % email)

        return redirect("/")
    #if email and password does not match what's in the system, redirect to login
    else:
        flash("That email and password combination does not exist in the system.")
        return redirect("/login")

@app.route('/logout')
def logout_user():
    """Logout user."""

    #remove user from the session
    session.pop("current_user", None)
    print session

    flash("Logged out.")

    return redirect("/")


@app.route('/new-user')
def show_new_user_page():
    """Show new user form."""

    return render_template("new_user.html")


@app.route('/create-new-user', methods=['POST'])
def create_new_user():
    """Create new user."""

    #get email and password from form and save as variables
    email = request.form.get("email")
    password = request.form.get("password")

    #run query to check if email is already in the database
    emails = User.query.filter(User.email==email).all()

    #if it returns a row containing the email, redirect user to page again 
    if emails:
        flash("That email is already in the system.")
        return redirect("/new-user")
    #else add the new user information to the table
    else:
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
        user = User(email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        print session
        return redirect("/login")


@app.route('/search-results')
def show_results():
    """Search results page."""

    #get the search bar input and save as a variable
    search = request.args.get("search")
    #turn unicode in string
    search = str(search)
    #encode search
    encoded_search = urllib2.quote(search)
    #API call using title of series, producing results that are close to the search 
    results = guidebox_search_title(encoded_search)

    return render_template("search_results.html", results=results)


@app.route('/show/<guidebox_id>')
def series_information(guidebox_id):
    """Show page containing basic information about the series and where a user can watch the series online and on cable TV."""

    #gathering information regarding the show
    show_info = guidebox_show_info(guidebox_id)

    #gathering information about the show's seasons
    seasons_results = guidebox_season_info(guidebox_id)

    #gathering information about where the show's available online
    all_streaming_sources = guidebox_streaming_sources_info(guidebox_id)

    #get show title from Guidebox so it can be used in the OnConnect title search url 
    show_title = str(show_info["title"])

    #obtaining the OnConnect seriesId that will be used in the OnConnect series airings url
    series_id = onconnect_search_series_id(show_title)

    #obtaining listing information for a 24 hour period from the current time
    airings = onconnect_search_airings(series_id)

    if "current_user" in session:
        #find the current logged in user
        user_email = session["current_user"]

        #use email to find the user_id
        user_id = db.session.query(User.user_id).filter(User.email==user_email).all()

        #check if user has favorited show already
        favorite = Favorite.query.filter_by(guidebox_id=guidebox_id, user_id=user_id[0]).all()

        #if user has favorited, send back "&#10003; Favorite"
        if favorite:
            favorited = True
        #if has not favorited yet, send back just "Favorite"
        else:
            favorited = False
    else:
        favorited = False

    return render_template("show_page.html",
                            show_info=show_info, 
                            seasons_results=seasons_results,
                            all_streaming_sources=all_streaming_sources,
                            airings=airings,
                            favorited=favorited)


@app.route('/save_to_favorites', methods=['POST'])
def save_to_favorites_list():
    """Save show to user's favorites list."""

    #get show id from the event handler/post request
    show_id = str(request.form.get("id"))
    #get button content from the event handler/post request
    button_content = request.form.get("button_content")
    button_content_encoded = button_content.encode('utf-8')

    #save utf-8 encoded checkmark as a string variable
    check_mark = "\xe2\x9c\x93"

    #find the current logged in user
    user_email = session["current_user"]

    #use email to find the user_id
    user_id = db.session.query(User.user_id).filter(User.email==user_email).one()
    #if the show has not been favorited yet
    if check_mark not in button_content_encoded:
        #add row in favorites table
        favorite = Favorite(guidebox_id=show_id, user_id=user_id)
        db.session.add(favorite)
        db.session.commit()
        #pass back the show_id and that the show has been favorited
        payload = {"show_id":show_id,"favorite":"True"}
        return jsonify(payload)
    else:
        #delete row in favorites table
        Favorite.query.filter_by(guidebox_id=show_id).delete()
        db.session.commit()
        #pass back the show_id and that the show has been unfavorited
        payload = {"show_id":show_id,"favorite":"False"}
        return jsonify(payload)

@app.route('/user-profile')
def show_user():
    """Show user's profile."""

    #get user email from session
    email = session["current_user"]

    #get user_id to get access to favorites table and users table
    user_id = User.query.filter(User.email==email).first()

    return render_template("user_profile.html", user_id=user_id)


##########################################################################

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0")

