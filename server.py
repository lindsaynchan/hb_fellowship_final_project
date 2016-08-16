"""Television listings and streaming search."""

import os
from jinja2 import StrictUndefined
from flask import Flask, render_template, request, flash, redirect, session
from model import connect_to_db, db, User, Show, StreamingService, Favorite, CableListing, Streaming, Network
from guidebox import guidebox_search_title, guidebox_show_info, guidebox_season_info, guidebox_streaming_sources_info
from onconnect import onconnect_search_series_id, onconnect_search_airings
import requests
import urllib2
import arrow


GUIDEBOX_BASE_URL = "http://api-public.guidebox.com/v1.43/US/"

app = Flask(__name__)

app.secret_key = os.environ.get('APP_KEY')
GUIDEBOX_API_KEY = os.environ.get('GUIDEBOX_API_KEY')
ONCONNECT_API_KEY = os.environ.get('ONCONNECT_API_KEY')

app.jinja_env.undefined = StrictUndefined

##########################################################################


@app.route('/')
def show_index():
    """Homepage."""

    return render_template("homepage.html")

@app.route('/login')
def show_login_page():
    """Login page."""

    return render_template("login.html")

@app.route('/new-user')
def show_new_user_page():
    """Create new user page."""

    email = request.args.get("email")
    password = request.args.get("password")

    db.session.execute("INSERT INTO users VALUES (email, password)")
    db.session.commit()

    return render_template("new_user.html")

@app.route('/login-user')
def login_user():
    """Login user."""

    email = request.args.get("email")
    password = request.args.get("password")
    session["user"] = email

    print session

    return redirect("/")

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

    return render_template("show_page.html",
                            show_info=show_info, 
                            seasons_results=seasons_results,
                            all_streaming_sources=all_streaming_sources,
                            airings=airings)


@app.route('/save_to_favorites', methods=['POST'])
def save_to_favorites_list():
    """Save show to user's favorites list."""

    #get show id from the event handler/post request
    show_id = str(request.form.get("id"))

    user_id = session["user"]

    #add in row of favorites table using show id and user id
    db.session.execute("INSERT INTO favorites VALUES (show_id,user_id)")
    db.session.commit()

    return show_id

@app.route('/user/<user_id>')
def show_user(user_id):
    """Show user's profile."""

    return render_template("user_profile.html")


##########################################################################

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0")

