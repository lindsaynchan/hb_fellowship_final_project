"""Television listings and streaming search."""

import os
from jinja2 import StrictUndefined
from flask import Flask, render_template, request, flash, redirect, session
from model import connect_to_db, db, User, Show, StreamingService, Favorite, CableListing, Streaming, Network
from guidebox import guidebox_search_title, guidebox_show_info, guidebox_season_info, guidebox_streaming_sources_info
from onconnect import onconnect_search_series_id, onconnect_search_airings
import requests
import urllib2

GUIDEBOX_BASE_URL = "http://api-public.guidebox.com/v1.43/US/"

app = Flask(__name__)

app.secret_key = os.environ.get('APP_KEY')
GUIDEBOX_API_KEY = os.environ.get('GUIDEBOX_API_KEY')
ONCONNECT_API_KEY = os.environ.get('ONCONNECT_API_KEY')

app.jinja_env.undefined = StrictUndefined

##########################################################################

#creating homepage route to return homepage.html
@app.route('/')
def show_index():
    """Homepage."""

    return render_template("homepage.html")

#creating search results route that will show series results from Guidebox API 
#call
@app.route('/search-results')
def show_results():
    """Search results page."""

    #get the search bar input and save as a variable
    search = request.args.get("search")
    #turn unicode in string
    search = str(search)
    #encode search
    encoded_search = urllib2.quote(search)

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

    airings = onconnect_search_airings(series_id)

    return render_template("show_page.html",
                            show_info=show_info, 
                            seasons_results=seasons_results,
                            all_streaming_sources=all_streaming_sources)

# @app.route('/user/<user_id>')
# def index(user_id):
#     """Show user's profile."""

#     return render_template("show_profile.html")


##########################################################################

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0")

